"""Parameter sweep generator."""

from enum import Enum
from itertools import product
from typing import List, Optional

import pandas as pd

from population_data_analysis.common import BasePydanticForRepo, deduplicate_list


class SweepType(str, Enum):
    """Type of sweep."""

    int = "int"
    float = "float"
    bool = "bool"
    string = "string"


class SweepConfig(BasePydanticForRepo):
    """Sweep configuration."""

    hard_coded_choices: Optional[List[any]] = None
    min: Optional[float] = None
    max: Optional[float] = None
    samples: Optional[int] = None
    default: Optional[any] = None
    type: Optional[SweepType] = None


class SweepIterators:
    """Sweep iterators."""

    def convert_sweep_config_to_actual_choices(self, sweep_config: SweepConfig):
        """Make an iteration for parameters sweeping."""
        choices_for_ablation = []
        choices_to_vary_for_other_ablations = []
        if sweep_config.hard_coded_choices is not None:
            choices_for_ablation = sweep_config.hard_coded_choices
        elif sweep_config.type is None:
            if sweep_config.default == "None":
                choices_for_ablation.append(None)
            else:
                choices_for_ablation = [sweep_config.default]
        elif sweep_config.type == "int":
            for i in range(sweep_config.samples):
                new_value = int(
                    sweep_config.min
                    + i
                    * (sweep_config.max - sweep_config.min)
                    / (sweep_config.samples - 1)
                )
                choices_for_ablation.append(new_value)
        if sweep_config.default == "None":
            choices_to_vary_for_other_ablations.append(None)
        elif sweep_config.default is not None:
            choices_to_vary_for_other_ablations.append(sweep_config.default)
        else:
            choices_to_vary_for_other_ablations = choices_for_ablation
        return deduplicate_list(choices_for_ablation), deduplicate_list(
            choices_to_vary_for_other_ablations
        )

    def make_multi_parameter_search(self, sweep_config_list: List[List[SweepConfig]]):
        """Make a multi-parameter search."""
        ablation_sets = {}
        alternatives = {}  # Configs with a default value.
        # Build dictionaries for fixed and variable parameters.
        for idx, sweep_config in enumerate(sweep_config_list):
            choices_for_ablation, choices_to_vary_for_other_ablations = (
                self.convert_sweep_config_to_actual_choices(sweep_config)
            )
            ablation_sets[idx] = choices_for_ablation
            alternatives[idx] = choices_to_vary_for_other_ablations

        full_set = []
        for idx, choices_for_ablation in ablation_sets.items():
            alternatives_list = {
                idx2: alts
                for idx2, alts in alternatives.items()
                if idx2 != idx and isinstance(alts, list)
            }
            alternatives_list[idx] = choices_for_ablation
            combinations = list(product(*alternatives_list.values()))
            # Create a DataFrame using the dictionary keys as column names.
            df = pd.DataFrame(combinations, columns=alternatives_list.keys())
            for idx2, alts in alternatives.items():
                if idx2 != idx and not isinstance(alts, list):
                    df[idx2] = alts
            full_set.append(df)

        joined_df = pd.concat(full_set, ignore_index=True)

        # remove duplicate rows
        # Step 1: Convert lists to tuples
        joined_df = joined_df.applymap(lambda x: tuple(x) if isinstance(x, list) else x)

        # Step 2: Drop duplicate rows
        df_unique = joined_df.drop_duplicates()

        # Step 3: Convert tuples back to lists
        df_unique = df_unique.map(lambda x: list(x) if isinstance(x, tuple) else x)
        df_unique = df_unique.sort_index(axis=1)
        return df_unique


sweep_iterator = SweepIterators()
