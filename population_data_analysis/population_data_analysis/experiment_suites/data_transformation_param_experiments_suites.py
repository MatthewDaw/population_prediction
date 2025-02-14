"""Suite for running all data_transformations configurations."""

from population_data_analysis.pipeline_operations.data_transformations.data_transformation_config_objects import (
    AvailableDataTransformationOperations,
    DataTransformationOptions,
)
from population_data_analysis.sweep_generation_tools.config_list_generation import (
    ParameterChoice,
    ParameterDecisionSuite,
)
from population_data_analysis.sweep_generation_tools.parameter_sweep_generator import (
    SweepConfig,
)

possible_transformations = [
    ParameterDecisionSuite(
        function_name=AvailableDataTransformationOperations.data_transformation,
        parameter_suite_name="full_sweep",
        associated_pydantic_model=DataTransformationOptions,
        parameter_choices=[
            ParameterChoice(
                parameter_name="z_normalize",
                parameter_value=SweepConfig(
                    hard_coded_choices=["always", "never", "conditional"],
                    default="always",
                ),
            ),
            ParameterChoice(
                parameter_name="log",
                parameter_value=SweepConfig(
                    hard_coded_choices=["always", "never", "conditional"],
                    default="always",
                ),
            ),
            ParameterChoice(
                parameter_name="difference",
                parameter_value=SweepConfig(
                    hard_coded_choices=["always", "never", "conditional"],
                    default="always",
                ),
            ),
            ParameterChoice(
                parameter_name="drop_near_constant_columns",
                parameter_value=SweepConfig(
                    hard_coded_choices=["always", "never"], default="always"
                ),
            ),
            ParameterChoice(
                parameter_name="train_test_split",
                parameter_value=SweepConfig(default=0.8),
            ),
        ],
    ),
    ParameterDecisionSuite(
        function_name=AvailableDataTransformationOperations.data_transformation,
        parameter_suite_name="best_guess",
        associated_pydantic_model=DataTransformationOptions,
        parameter_choices=[
            ParameterChoice(
                parameter_name="z_normalize",
                parameter_value=SweepConfig(default="always"),
            ),
            ParameterChoice(
                parameter_name="log", parameter_value=SweepConfig(default="always")
            ),
            ParameterChoice(
                parameter_name="difference",
                parameter_value=SweepConfig(default="always"),
            ),
            ParameterChoice(
                parameter_name="drop_near_constant_columns",
                parameter_value=SweepConfig(default="always"),
            ),
            ParameterChoice(
                parameter_name="train_test_split",
                parameter_value=SweepConfig(default=0.8),
            ),
        ],
    ),
]
