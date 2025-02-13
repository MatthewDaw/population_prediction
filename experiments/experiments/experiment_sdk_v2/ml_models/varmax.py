"""VARMAX ML Model Container."""

import pandas as pd
from statsmodels.tsa.statespace.varmax import VARMAX
from experiments.experiment_sdk_v2.ml_models.parent_ml_model_template import ParentMLModelTemplate, \
    MLHyperparametersTemplate
from experiments.experiment_sdk_v2.submodels.sweep_iterators import SweepConfig, sweep_iterator

class VARMAXHyperparameters(MLHyperparametersTemplate):
    """Hyperparameters for the VARMAX model."""

    p: int = 1
    q: int = 1

    def get_all_sweeps(self):
        """Get all possible instantiations of the hyperparameters."""
        parameter_set = []
        p_sweep = SweepConfig(min=1,max=6,samples=10,default=1,type='int')
        q_sweep = SweepConfig(min=1,max=6,samples=10,default=1,type='int')
        combinations_dataframe = sweep_iterator.make_multi_parameter_search([p_sweep, q_sweep])
        for index, row in combinations_dataframe.iterrows():
            parameter_set.append(VARMAXHyperparameters(p=row[0], q=row[1]))
        return parameter_set


class VARMAXMLModelContainer(ParentMLModelTemplate):
    """VARMAX ML model container."""

    def __init__(self, hyperparameters: VARMAXHyperparameters):
        """Initialize the class with hyperparameters."""
        super().__init__()
        self.model = None
        self.fit_model = None
        self.training_data = None
        self.order = (hyperparameters.p, hyperparameters.q)

    def fit(self, data: pd.DataFrame):
        """Train the VARMAX model."""
        self.model = VARMAX(data, order=self.order)
        self.fit_model = self.model.fit(disp=False)
        self.training_data = data

    def forecast(self, steps: int):
        """Predict future values using the fitted model."""
        if self.fit_model is None:
            raise ValueError("The model must be fitted before forecasting.")
        forecast_result = self.fit_model.get_forecast(steps=steps)
        return forecast_result.predicted_mean

    def generate_confidence_bounds(self, steps: int, alpha: float = 0.05):
        """Generate confidence bounds for the forecast."""
        if self.fit_model is None:
            raise ValueError("The model must be fitted before generating confidence bounds.")
        forecast_result = self.fit_model.get_forecast(steps=steps)
        conf_int = forecast_result.conf_int(alpha=alpha)
        return conf_int

    def summary(self):
        """Return the model summary."""
        if self.fit_model is None:
            return "No summary available. The model has not been fitted yet."
        return self.fit_model.summary()
