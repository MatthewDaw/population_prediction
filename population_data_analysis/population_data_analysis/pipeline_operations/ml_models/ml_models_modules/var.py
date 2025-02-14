"""VAR Ml model container."""

import mlflow
import numpy as np
import pandas as pd
from statsmodels.tsa.api import VAR

from population_data_analysis.pipeline_operations.ml_models.ml_models_config_objects import (
    VARHyperparameters,
)


class VARMLModelContainer:
    """VAR Ml model container."""

    def __init__(self, hyperparameters: VARHyperparameters):
        """Initialize the class."""
        self.model = None
        self.fit_model = None
        self.training_data = None
        self.p = hyperparameters.p

    def fit_forecast(self, data: pd.DataFrame, steps: int) -> np.ndarray:
        """Train the model."""
        self.model = VAR(data)
        self.fit_model = self.model.fit(self.p)
        self.training_data = data
        forecast = self.fit_model.forecast(
            self.training_data.values[-1 * self.p :], steps=steps
        )
        signature = mlflow.models.infer_signature(data, forecast)
        mlflow.statsmodels.log_model(
            self.fit_model, "statsmodels_model", signature=signature
        )
        return forecast

    def generate_confidence_bounds(self, steps: int):
        """Generate confidence bounds."""
        forcast, lower_bound, upper_bound = self.fit_model.forecast_interval(
            self.model.endog[-self.p :], steps=steps
        )
        return forcast, lower_bound, upper_bound
