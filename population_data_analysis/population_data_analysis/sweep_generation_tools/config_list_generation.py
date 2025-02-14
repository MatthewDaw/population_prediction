"""Get all possible run configs to experiment on."""

from collections import defaultdict
from typing import Any, Dict, List

import pandas as pd

from population_data_analysis.common import BasePydanticForRepo
from population_data_analysis.sweep_generation_tools.parameter_sweep_generator import (
    SweepConfig,
    sweep_iterator,
)


class ParameterChoice(BasePydanticForRepo):
    """Parameter choice."""

    parameter_name: str
    parameter_value: SweepConfig = SweepConfig(default=None)


class ParameterDecisionSuite(BasePydanticForRepo):
    """Database retrival source."""

    function_name: str
    parameter_suite_name: str
    associated_pydantic_model: Any
    parameter_choices: List[ParameterChoice]


def custom_check_if_none(value):
    """Check if value is none, need to do this mostly just because pandas makes np.null values for some dumb reason."""
    if value is None:
        return True
    if isinstance(value, list):
        return False
    if pd.isna(value):
        return True
    return False


def generate_all_possible_sweeps(top_level_choices: List) -> Dict:
    """Generate all possible sweeps."""

    decision_sets = defaultdict(list)
    for retrival_source in top_level_choices:
        parameter_sweep_for_specific_data_source = (
            sweep_iterator.make_multi_parameter_search(
                [el.parameter_value for el in retrival_source.parameter_choices]
            )
        )
        column_names = [el.parameter_name for el in retrival_source.parameter_choices]
        parameter_sweep_for_specific_data_source.columns = column_names
        converted_to_pydantic_objects = []
        for _, row in parameter_sweep_for_specific_data_source.iterrows():
            row_with_right_nones = {
                k: None if custom_check_if_none(v) else v
                for k, v in row.to_dict().items()
            }
            converted_to_pydantic_objects.append(
                retrival_source.associated_pydantic_model(**row_with_right_nones)
            )
        decision_sets[retrival_source.function_name] += converted_to_pydantic_objects
    return decision_sets
