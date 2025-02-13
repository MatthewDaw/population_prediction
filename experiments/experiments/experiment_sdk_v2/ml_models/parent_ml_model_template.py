"""Parent ML model template for all experiments."""

from pydantic import BaseModel

class MLHyperparametersTemplate(BaseModel):
    """Parent class for all hyperparameters."""

    def get_all_sweeps(self):
        """Get all possible instantiations of the hyperparameters."""
        raise NotImplementedError

class ParentMLModelTemplate:
    """Parent ML model template for all experiments."""

    def fit(self, data):
        """Train the model."""
        raise NotImplementedError

    def forcast(self, steps: int):
        """Predict on the model."""
        raise NotImplementedError

    def generate_confidence_bounds(self, data):
        """Generate confidence bounds."""
        raise NotImplementedError

    def get_possible_sweep_configs(self):
        """Get all possible sweep configurations."""
        raise NotImplementedError