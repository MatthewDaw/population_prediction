"""VAR Ml model container."""
# from experiments.experiment_sdk_v2.ml_models.model_hyperparameters import VARHyperparameters
from experiments.experiment_sdk_v2.ml_models.parent_ml_model_template import ParentMLModelTemplate, \
    MLHyperparametersTemplate
import pandas as pd
from statsmodels.tsa.api import VAR
from pydantic import BaseModel

from experiments.experiment_sdk_v2.submodels.sweep_iterators import SweepConfig, sweep_iterator


class VARHyperparameters(MLHyperparametersTemplate):
    """Hyperparameters for the VAR model."""

    p: int = 1

    def get_all_sweeps(self):
        """Get all possible instantiations of the hyperparameters."""
        parameter_set = []
        for value in sweep_iterator.make_iteration(SweepConfig(min=1,max=10,samples=10,default=1,type='int')):
            parameter_set.append(VARHyperparameters(p=value))
        return parameter_set

class VARMLModelContainer(ParentMLModelTemplate):
    """VAR Ml model container."""

    def __init__(self, hyperparameters: VARHyperparameters):
        """Initialize the class."""
        super().__init__()
        self.model = None
        self.fit_model = None
        self.training_data = None
        self.p = hyperparameters.p

    def fit(self, data: pd.DataFrame):
        """Train the model."""
        self.model = VAR(data)
        self.fit_model = self.model.fit(self.p)
        self.training_data = data


    def forcast(self, steps: int):
        """Predict on the model."""
        return self.fit_model.forecast(self.training_data.values[-1*self.p:], steps=steps)

    def generate_confidence_bounds(self, steps: int):
        """Generate confidence bounds."""
        forcast, lower_bound, upper_bound = self.fit_model.forecast_interval(self.model.endog[-self.p:], steps=steps)
        return forcast, lower_bound, upper_bound


    def summary(self):
        """Return the model summary."""
        try:
            return self.fit_model.summary()
        except:
            return "No summary available."