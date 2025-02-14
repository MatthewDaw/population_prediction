"""Experiments pipeline SDK."""

import base64
import zlib
from typing import Union

import mlflow

from population_data_analysis.common import BasePydanticForRepo
from population_data_analysis.pipeline_operations.data_transformations.data_transformations_sdk import \
    DataTransformationsSDK
from population_data_analysis.pipeline_operations.ml_models.ml_models_sdk import MLModelsSDK

from population_data_analysis.pipeline_operations.data_transformations.data_transformation_config_objects import (
    AvailableDataTransformationOperations,
    DataTransformationOptions,
)
from population_data_analysis.pipeline_operations.evaluation.evaluation_config_objects import (
    AvailableEvaluationOperations,
    EvaluationConfig,
    EvaluationOutput,
)
from population_data_analysis.pipeline_operations.evaluation.evaluation_sdk import (
    TrainingProcedureSDK,
)
from population_data_analysis.pipeline_operations.ml_models.ml_models_config_objects import (
    AvailableMLOperations,
    VARHyperparameters,
    VARMAXHyperparameters,
)
from population_data_analysis.pipeline_operations.raw_dataset_loader.raw_data_loader_config_objects import \
    AvailableDataRetrivalOperations, RetrivalParameters


from population_data_analysis.pipeline_operations.raw_dataset_loader.raw_data_loader_sdk import (
    RawDataLoaderSDK,
)


class ExperimentRunConfig(BasePydanticForRepo):
    """Experiment run configuration."""

    raw_data_loader_operation_name: AvailableDataRetrivalOperations
    raw_data_loader_config: RetrivalParameters

    data_transformation_operation_name: AvailableDataTransformationOperations
    data_transformation_config: DataTransformationOptions

    ml_model_operation_name: AvailableMLOperations
    ml_model_config: Union[VARHyperparameters, VARMAXHyperparameters]

    evaluation_operation_name: AvailableEvaluationOperations
    evaluation_config: EvaluationConfig

    def dump_to_params(self):
        """Dump to params."""
        return {
            "raw_data_loader_operation_name": self.raw_data_loader_operation_name,
            "raw_data_loader_config": self.raw_data_loader_config.model_dump(),
            "data_transformation_operation_name": self.data_transformation_operation_name,
            "data_transformation": self.data_transformation_config.model_dump(),
            "ml_model_operation_name": self.ml_model_operation_name,
            "ml_model_config": self.ml_model_config.model_dump(),
            "evaluation_operation_name": self.evaluation_operation_name,
            "evaluation_config": self.evaluation_config.model_dump(),
        }

    def dump_to_tags(self):
        """Dump to tags."""
        return {
            "raw_data_loader_operation_name": self.raw_data_loader_operation_name,
            "data_transformation_operation_name": self.data_transformation_operation_name,
            "ml_model_operation_name": self.ml_model_operation_name,
            "evaluation_operation_name": self.evaluation_operation_name,
        }

    def dump_to_name(self) -> str:
        """Generate a compressed string representation of the model's values."""
        # Serialize the model's data to a JSON-formatted string
        json_data = self.model_dump_json()

        # Compress the JSON string using zlib
        compressed_data = zlib.compress(json_data.encode("utf-8"))

        # Encode the compressed data to a base64 string
        base64_encoded_data = base64.b64encode(compressed_data).decode("utf-8")

        return base64_encoded_data


class ExperimentsSDK:
    """Experiments SDK to run full training and evaluation pipelines."""

    def __init__(self):
        """Initialize the class."""

        self.raw_data_loader_sdk = RawDataLoaderSDK()
        self.ml_models_sdk = MLModelsSDK()
        self.data_transformation_sdk = DataTransformationsSDK()
        self.evaluations_sdk = TrainingProcedureSDK()

    def log_new_run_to_mlflow(self, experiment_config: ExperimentRunConfig):
        """Log a new run to mlflow."""

        mlflow.log_params(experiment_config.dump_to_params())
        run_tags = experiment_config.dump_to_tags()
        for tag_name, tag_value in run_tags.items():
            mlflow.set_tag(tag_name, tag_value)

    def run_experiment(self, config: ExperimentRunConfig) -> EvaluationOutput:
        """Run an experiment."""

        self.log_new_run_to_mlflow(config)

        data = self.raw_data_loader_sdk.run(
            retrival_parameters=config.raw_data_loader_config,
            operation=config.raw_data_loader_operation_name,
        )
        train_data, test_data = self.data_transformation_sdk.run(
            data, config.data_transformation_config
        )
        try:
            predictions = self.ml_models_sdk.run(
                train_data,
                len(test_data),
                config.ml_model_operation_name,
                config.ml_model_config,
            )
        except Exception as e:  # pylint: disable=broad-exception-caught
            self.evaluations_sdk.log_failed_run(str(e))
            return EvaluationOutput(
                failed=False,
                error_message=str(e),
            )
        evaluation = self.evaluations_sdk.run(
            test_data, predictions, config.evaluation_config
        )
        return evaluation
