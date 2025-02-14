"""Raw database load experiments suites."""

from population_data_analysis.pipeline_operations.raw_dataset_loader.raw_data_loader_config_objects import (
    AvailableDataRetrivalOperations,
    RetrivalParameters,
)
from population_data_analysis.sweep_generation_tools.config_list_generation import (
    ParameterChoice,
    ParameterDecisionSuite,
)
from population_data_analysis.sweep_generation_tools.parameter_sweep_generator import (
    SweepConfig,
)

possible_retrival_sources = [
    ParameterDecisionSuite(
        parameter_suite_name="averaged_across_states",
        function_name=AvailableDataRetrivalOperations.averaged_across_states,
        associated_pydantic_model=RetrivalParameters,
        parameter_choices=[
            ParameterChoice(
                parameter_name="specific_states",
                parameter_value=SweepConfig(default="None"),
            ),
            ParameterChoice(
                parameter_name="random_sample_n_states",
                parameter_value=SweepConfig(default="None"),
            ),
        ],
    ),
    ParameterDecisionSuite(
        parameter_suite_name="full_database",
        function_name=AvailableDataRetrivalOperations.full_database,
        associated_pydantic_model=RetrivalParameters,
        parameter_choices=[
            ParameterChoice(
                parameter_name="specific_states",
                parameter_value=SweepConfig(
                    hard_coded_choices=[None, ["Utah", "Idaho"]], default="None"
                ),
            ),
            ParameterChoice(
                parameter_name="random_sample_n_states",
                parameter_value=SweepConfig(
                    hard_coded_choices=[None, 1, 2], default="None"
                ),
            ),
        ],
    ),
]
