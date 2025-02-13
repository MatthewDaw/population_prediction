"""Performance measurer module."""

from experiments.experiment_sdk_v2.ml_models.model_hyperparameters import SweepConfig
from experiments.experiment_sdk_v2.ml_models.model_retriever import retrieve_model
from experiments.experiment_sdk_v2.submodels.data_loader import DataLoader
from experiments.experiment_sdk_v2.submodels.experiment_parameters import ExperimentConfig
from sklearn.metrics import mean_squared_error, mean_absolute_error
import copy

from experiments.experiment_sdk_v2.submodels.sweep_iterators import SweepIterators

from pydantic import BaseModel, ConfigDict
import pandas as pd
from typing import Optional
import numpy as np

class PerformanceResults(BaseModel):
    """Performance results class."""

    model_config = ConfigDict(arbitrary_types_allowed=True)  # Pydantic v2 syntax

    loss: float
    loss_metric: str
    lower_bounds: Optional[np.array] = None
    upper_bounds: Optional[np.array] = None
    model_summary: Optional[str] = None


class PerformanceMeasurer:
    """Performance measurer class."""

    def __init__(self):
        """Initialize the class."""
        self.data_loader = DataLoader()
        self.seep_iterators = SweepIterators()

    def run_trial(self, data: pd.DataFrame, experiment_config: ExperimentConfig):
        """Run a single trial."""
        model = retrieve_model(experiment_config.ml_model_config)
        num_time_steps = len(data)
        train_end = int(num_time_steps * experiment_config.training_parameters.train_percentage)
        train_data = data.iloc[:train_end]
        val_data = data.iloc[train_end:]
        model.fit(train_data)
        predictions, lower_bounds, upper_bounds = model.generate_confidence_bounds(steps=len(val_data))
        if experiment_config.training_parameters.loss_metric == "mse":
            return PerformanceResults(
                loss=mean_squared_error(val_data, predictions),
                loss_metric="mse",
                lower_bounds=lower_bounds,
                upper_bounds=upper_bounds,
                model_summary=model.summary()
            )
        elif experiment_config.training_parameters.loss_metric == "mae":
            return PerformanceResults(
                loss=mean_absolute_error(val_data, predictions),
                loss_metric="mae",
                lower_bounds=lower_bounds,
                upper_bounds=upper_bounds,
                model_summary=model.summary()
            )
        raise ValueError("Invalid loss metric")

    def run_hyper_parameter_sweep(self, data: pd.DataFrame, experiment_config: ExperimentConfig):
        """Run a parameter search."""
        pass

    def execute_sweep(self, experiment_config: ExperimentConfig):
        """Execute a parameter sweep."""
        raw_data, normalized_data = self.data_loader.get_dataset(experiment_config.data_loader_parameters)
        hyperparameters_copy = copy.deepcopy(experiment_config.ml_model_config.hyperparameters)
        dict_defaults = {}
        for key, value in hyperparameters_copy.model_dump().items():
            if isinstance(value, dict):
                dict_defaults[key] = value['default']
            else:
                dict_defaults[key] = value
        optimal_sweep_choices = {}
        default_parameters = type(hyperparameters_copy)(**dict_defaults)
        for key, value in hyperparameters_copy.model_dump().items():
            if isinstance(value, dict):
                best_loss = float("inf")
                sweep_config = SweepConfig(**value)
                for new_value in self.seep_iterators.make_iteration(sweep_config):
                    hyperparameters_for_iteration = copy.deepcopy(default_parameters)
                    setattr(hyperparameters_for_iteration, key, new_value)
                    experiment_config.ml_model_config.hyperparameters = hyperparameters_for_iteration
                    try:
                        performance_result = self.run_trial(normalized_data, experiment_config)
                    except Exception as e:
                        print(f"Error: {e}")
                        continue
                    if performance_result.loss < best_loss:
                        best_parameter = new_value
                        best_loss = performance_result.loss
                        optimal_sweep_choices[key] = best_parameter
                if best_loss == float("inf"):
                    return PerformanceResults(
                        loss=float("inf"),
                        loss_metric=experiment_config.training_parameters.loss_metric,
                        lower_bounds=None,
                        upper_bounds=None,
                        model_summary=None
                    )
        final_parameters_defaults = {}
        for key, value in hyperparameters_copy.model_dump().items():
            if isinstance(value, dict):
                final_parameters_defaults[key] = optimal_sweep_choices[key]
            else:
                final_parameters_defaults[key] = value
        experiment_config.ml_model_config.hyperparameters = type(hyperparameters_copy)(**final_parameters_defaults)
        return self.run_trial(normalized_data, experiment_config)
