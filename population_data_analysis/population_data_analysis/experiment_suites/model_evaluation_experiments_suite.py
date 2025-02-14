"""Training setup experiments suite."""

from population_data_analysis.pipeline_operations.evaluation.evaluation_config_objects import (
    AvailableEvaluationOperations,
    EvaluationConfig,
)
from population_data_analysis.sweep_generation_tools.config_list_generation import (
    ParameterChoice,
    ParameterDecisionSuite,
)
from population_data_analysis.sweep_generation_tools.parameter_sweep_generator import (
    SweepConfig,
)

training_setup_suites = [
    ParameterDecisionSuite(
        function_name=AvailableEvaluationOperations.evaluate_model,
        parameter_suite_name="standard_evaluation",
        associated_pydantic_model=EvaluationConfig,
        parameter_choices=[
            ParameterChoice(
                parameter_name="metrics",
                parameter_value=SweepConfig(default=["mse", "mae"]),
            ),
        ],
    ),
]
