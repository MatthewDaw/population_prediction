"""VARMAX model container for the population data analysis pipeline."""

import mlflow
import numpy as np
import pandas as pd
from statsmodels.tsa.statespace.varmax import VARMAX

from population_data_analysis.pipeline_operations.ml_models.ml_models_config_objects import (
    VARMAXHyperparameters,
)


class VARMAXMLModelContainer:
    """VARMAX ML model container."""

    def __init__(self, hyperparameters: VARMAXHyperparameters):
        """Initialize the container using hyperparameters for a VARMAX model."""
        self.model = None
        self.fit_model = None
        self.training_data = None
        self.p = hyperparameters.p
        self.q = hyperparameters.q
        # Use the provided trend or default to a constant trend.
        self.trend = hyperparameters.trend

    def fit_forecast(self, data: pd.DataFrame, steps: int) -> np.ndarray:
        """
        Fit the VARMAX model and generate an out-of-sample forecast.

        Parameters:
            data (pd.DataFrame): The training time series data.
            steps (int): Number of steps to forecast ahead.

        Returns:
            np.ndarray: The forecasted values.
        """
        # Initialize the VARMAX model.
        self.model = VARMAX(data, order=(self.p, self.q), trend=self.trend)
        # Fit the model. (Additional fit options can be passed if needed.)
        self.fit_model = self.model.fit(disp=False)
        self.training_data = data
        # Generate forecast using get_forecast (which returns a PredictionResults object)
        forecast_results = self.fit_model.get_forecast(steps=steps)
        forecast = forecast_results.predicted_mean
        # Infer the model signature and log the fitted model using MLflow's statsmodels flavor.
        signature = mlflow.models.infer_signature(data, forecast)
        mlflow.statsmodels.log_model(
            self.fit_model, "statsmodels_model", signature=signature
        )
        return forecast

    def generate_confidence_bounds(self, steps: int, alpha: float = 0.05):
        """
        Generate prediction intervals for the forecast.

        Parameters:
            steps (int): Number of steps ahead for which to compute intervals.
            alpha (float): Significance level (default 0.05).

        Returns:
            tuple: (forecast, confidence_intervals) where confidence_intervals is a DataFrame.
        """
        # Re-obtain forecast results to compute intervals.
        forecast_results = self.fit_model.get_forecast(steps=steps)
        forecast = forecast_results.predicted_mean
        # For VARMAX models the conf_int method returns intervals for all endogenous variables.
        conf_int = forecast_results.conf_int(alpha=alpha)
        return forecast, conf_int
