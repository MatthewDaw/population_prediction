"""Iterate through all needed experiments."""

from collections import defaultdict
from itertools import product
from typing import List

import pandas as pd

from population_data_analysis.common import BasePydanticForRepo
from population_data_analysis.experiment_suites.data_transformation_param_experiments_suites import (
    possible_transformations,
)
from population_data_analysis.experiment_suites.model_evaluation_experiments_suite import (
    training_setup_suites,
)
from population_data_analysis.experiment_suites.models_experiments_suite import (
    model_parameter_suites,
)
from population_data_analysis.experiment_suites.raw_database_load_experiments_suites import (
    possible_retrival_sources,
)
from population_data_analysis.pipeline_operations.experiments_pipeline_sdk import (
    ExperimentRunConfig,
)
from population_data_analysis.sweep_generation_tools.config_list_generation import (
    generate_all_possible_sweeps,
)


class ModelSweepSetup(BasePydanticForRepo):
    """Model sweep setup."""

    experiment_name: str
    experiment_run_configs: List[ExperimentRunConfig]


class ModelParameterIterator:
    """Iterate through all needed experiments."""

    def _insert_new_layer_suite(self, stacked_configs, layer_name, layer_suite):
        """Insert a new layer suite."""
        for function_name, associated_pydantic_model in layer_suite.items():
            stacked_configs["layer_name"].append(layer_name)
            stacked_configs["function_name"].append(function_name)
            stacked_configs["associated_pydantic_model"].append(
                associated_pydantic_model
            )
        return stacked_configs

    def generate_basic_var_sweep(self) -> ModelSweepSetup:
        """Generate all possible parameters."""
        stacked_configs = {
            "layer_name": [],
            "function_name": [],
            "associated_pydantic_model": [],
        }
        database_related_configs = generate_all_possible_sweeps(
            possible_retrival_sources
        )
        stacked_configs = self._insert_new_layer_suite(
            stacked_configs, "raw_data_load_layer", database_related_configs
        )

        data_transformations_configs = generate_all_possible_sweeps(
            possible_transformations
        )
        stacked_configs = self._insert_new_layer_suite(
            stacked_configs, "data_transformation_layer", data_transformations_configs
        )

        model_configs = generate_all_possible_sweeps(model_parameter_suites)
        stacked_configs = self._insert_new_layer_suite(
            stacked_configs, "ml_model_layer", model_configs
        )

        training_setup_configs = generate_all_possible_sweeps(training_setup_suites)
        stacked_configs = self._insert_new_layer_suite(
            stacked_configs, "evaluation_layer", training_setup_configs
        )

        stacked_config_obj = pd.DataFrame(stacked_configs)

        configs_sorted_for_grouping = defaultdict(list)

        for layer_name, layer_suite in stacked_config_obj.groupby("layer_name"):
            for _, row in layer_suite.iterrows():
                for pydantic_model in row.associated_pydantic_model:
                    configs_sorted_for_grouping[layer_name].append(
                        (layer_name, row.function_name, pydantic_model)
                    )

        # Generate all possible combinations
        combinations = list(product(*configs_sorted_for_grouping.values()))

        experiment_run_configs = []
        for combination_set in combinations:
            set_as_dictionary = {
                c_set[0]: (c_set[1], c_set[2]) for c_set in combination_set
            }
            experiment_run_config = ExperimentRunConfig(
                raw_data_loader_operation_name=set_as_dictionary["raw_data_load_layer"][
                    0
                ],
                raw_data_loader_config=set_as_dictionary["raw_data_load_layer"][1],
                data_transformation_operation_name=set_as_dictionary[
                    "data_transformation_layer"
                ][0],
                data_transformation_config=set_as_dictionary[
                    "data_transformation_layer"
                ][1],
                ml_model_operation_name=set_as_dictionary["ml_model_layer"][0],
                ml_model_config=set_as_dictionary["ml_model_layer"][1],
                evaluation_operation_name=set_as_dictionary["evaluation_layer"][0],
                evaluation_config=set_as_dictionary["evaluation_layer"][1],
            )
            experiment_run_configs.append(experiment_run_config)

        return ModelSweepSetup(
            experiment_name="Simple VAR Model Sweep",
            experiment_run_configs=experiment_run_configs,
        )
