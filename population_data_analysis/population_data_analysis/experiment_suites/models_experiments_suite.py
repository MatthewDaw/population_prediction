"""Model experiments suite for the population data analysis project."""

from population_data_analysis.pipeline_operations.ml_models.ml_models_config_objects import (
    AvailableMLOperations,
    VARHyperparameters,
    VARMAXHyperparameters,
)
from population_data_analysis.sweep_generation_tools.config_list_generation import (
    ParameterChoice,
    ParameterDecisionSuite,
)
from population_data_analysis.sweep_generation_tools.parameter_sweep_generator import (
    SweepConfig,
)

model_parameter_suites = [
    ParameterDecisionSuite(
        function_name=AvailableMLOperations.var,
        parameter_suite_name="standard_var",
        associated_pydantic_model=VARHyperparameters,
        parameter_choices=[
            ParameterChoice(
                parameter_name="p",
                parameter_value=SweepConfig(
                    type="int", min=1, max=6, samples=6, default=3
                ),
            ),
        ],
    ),
    # ParameterDecisionSuite(
    #     function_name=AvailableMLOperations.varmax,
    #     parameter_suite_name="standard_varmax",
    #     associated_pydantic_model=VARMAXHyperparameters,
    #     parameter_choices=[
    #         ParameterChoice(
    #             parameter_name="p",
    #             parameter_value=SweepConfig(
    #                 type="int", min=1, max=6, samples=6, default=3
    #             ),
    #         ),
    #         ParameterChoice(
    #             parameter_name="q",
    #             parameter_value=SweepConfig(
    #                 type="int", min=1, max=6, samples=6, default=3
    #             ),
    #         ),
    #         ParameterChoice(
    #             parameter_name="trend",
    #             parameter_value=SweepConfig(
    #                 hard_coded_choices=["c", "trend"], default="c"
    #             ),
    #         ),
    #     ],
    # ),
]
