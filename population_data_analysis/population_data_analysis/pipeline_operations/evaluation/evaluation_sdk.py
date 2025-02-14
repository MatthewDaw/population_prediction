"""Evaluations SDK for data analysis."""

import mlflow
import numpy as np
import pandas as pd

from population_data_analysis.pipeline_operations.evaluation.evaluation_config_objects import (
    EvaluationConfig,
    EvaluationOutput,
)


class TrainingProcedureSDK:
    """Evaluations SDK for data analysis."""

    def log_failed_run(self, error_message: str):
        """Log a failed run."""
        mlflow.log_metric("successful_fit", False)
        mlflow.log_param("error_message", error_message)

    def run(
        self, test_data: pd.DataFrame, predictions: np.ndarray, config: EvaluationConfig
    ):
        """Run the evaluation."""

        mse = None
        mae = None

        # Calculate the error
        if "mse" in config.metrics:
            mse = np.mean((test_data - predictions) ** 2)
            mlflow.log_metric("mse", mse)
            print(f"Mean squared error: {mse}")
        if "mae" in config.metrics:
            mae = np.mean(np.abs(test_data - predictions))
            mlflow.log_metric("mae", mae)
            print(f"Mean absolute error: {mae}")

        mlflow.log_metric("successful_fit", True)

        print(f"Successfully fitted and evaluated the model. MSE: {mse}, MAE: {mae}")

        return EvaluationOutput(failed=False, error_message=None, mse=mse, mae=mae)
