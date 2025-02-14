"""SDK for ML models operations."""

from typing import Union

import numpy as np
import pandas as pd

from population_data_analysis.pipeline_operations.ml_models.ml_models_config_objects import (
    AvailableMLOperations,
    VARHyperparameters,
    VARMAXHyperparameters,
)
from population_data_analysis.pipeline_operations.ml_models.ml_models_modules.var import (
    VARMLModelContainer,
)
from population_data_analysis.pipeline_operations.ml_models.ml_models_modules.varmax import (
    VARMAXMLModelContainer,
)


class MLModelsSDK:
    """SDK for ML models operations."""

    def run(
        self,
        train_data: pd.DataFrame,
        steps: int,
        operation: AvailableMLOperations,
        hyperparameters: Union[VARHyperparameters, VARMAXHyperparameters],
    ) -> np.ndarray:
        """Run an operation."""
        if operation == AvailableMLOperations.var:
            model = VARMLModelContainer(hyperparameters)
        elif operation == AvailableMLOperations.varmax:
            model = VARMAXMLModelContainer(hyperparameters)
        else:
            raise ValueError("Operation not found.")
        forecasted_values = model.fit_forecast(train_data, steps=steps)
        return forecasted_values
