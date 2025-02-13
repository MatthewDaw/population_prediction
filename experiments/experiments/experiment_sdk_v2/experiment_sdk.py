"""Experiments sdk for running experinemtns and finding the best possible model."""
import pandas as pd

from experiments.experiment_sdk_v2.submodels.data_loader import DataLoader
from experiments.experiment_sdk_v2.submodels.experiment_parameters import ExperimentConfig
from experiments.experiment_sdk_v2.submodels.performance_measurer import PerformanceMeasurer

from experiments.experiment_sdk_v2.submodels.sweep_iterators import SweepIterators


class ExperimentSDK:
    """Class for running experiments."""

    def __init__(self):
        """Initialize the class."""
        self.data_loader = DataLoader()
        self.performance_measurer = PerformanceMeasurer()
        self.seep_iterators = SweepIterators()

    def run_hyper_parameter_sweep(self, data: pd.DataFrame, experiment_config: ExperimentConfig):
        """Run a parameter search."""
        pass

    def execute_sweep(self, experiment_config: ExperimentConfig):
        """Execute a parameter sweep."""
        return self.performance_measurer.execute_sweep(experiment_config)

    def execute_experiment(self, experiment_config: ExperimentConfig):
        """Execute an experiment."""
        raw_data, normalized_data = self.data_loader.get_dataset(experiment_config.data_loader_parameters)
        # self.run_parameter_search(normalized_data, experiment_config)
