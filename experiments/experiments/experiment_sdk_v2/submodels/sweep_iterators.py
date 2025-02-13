"""Sweep iterator functions."""
from collections import defaultdict

from typing import List
from itertools import product
import pandas as pd
from pydantic import BaseModel
from typing import Optional

class SweepConfig(BaseModel):
    """Sweep configuration."""

    min: float
    max: float
    samples: Optional[int] = None
    default: float
    type: str = 'int'


class SweepIterators:

    def make_iteration(self, sweep_config: SweepConfig):
        """Make an iteration for parameters sweeping."""
        values_to_iterate = []
        if sweep_config.type == "int":
            for i in range(sweep_config.samples):
                new_value = int(sweep_config.min + i * (sweep_config.max - sweep_config.min) / (sweep_config.samples - 1))
                values_to_iterate.append(new_value)
        seen = set()
        deduplicated_values = [x for x in values_to_iterate if not (x in seen or seen.add(x))]
        for value in deduplicated_values:
            yield value

    def make_multi_parameter_search(self, sweep_config_list: List[SweepConfig]):
        """Make a multi-parameter search."""
        alternatives = {}  # Configs with a default value.

        # Build dictionaries for fixed and variable parameters.
        for idx, sweep_config in enumerate(sweep_config_list):
            if sweep_config.default is not None:
                alternatives[idx] = sweep_config.default
            else:
                # Ensure we have a list of values to iterate over.
                alternatives[idx] = list(self.make_iteration(sweep_config))

        full_set = []

        for idx, sweep_config in enumerate(sweep_config_list):
            root_possibilities = list(self.make_iteration(sweep_config))
            alternatives_list = {idx2: alts for idx2, alts in alternatives.items() if idx2 != idx and isinstance(alts, list)}
            alternatives_list[idx] = root_possibilities
            combinations = list(product(*alternatives_list.values()))
            # Create a DataFrame using the dictionary keys as column names.
            df = pd.DataFrame(combinations, columns=alternatives_list.keys())
            for idx2, alts in alternatives.items():
                if idx2 != idx and not isinstance(alts, list):
                    df[idx2] = alts
            full_set.append(df)
        joined = pd.concat(full_set)
        df_sorted = joined.sort_index(axis=1)
        return df_sorted


sweep_iterator = SweepIterators()