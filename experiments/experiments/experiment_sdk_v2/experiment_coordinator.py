"""Coordinator to trigger experiments and track their progress."""
from experiments.experiment_sdk_v2.experiment_sdk import ExperimentSDK
from experiments.experiment_sdk_v2.ml_models.model_hyperparameters import VARHyperparameters, SweepConfig, \
    VARMAXHyperparameters
from experiments.experiment_sdk_v2.submodels.experiment_parameters import ExperimentConfig, \
    DataTransformationOptions, DataLoaderParameters, AvailableModelsModelConfigs, AvailableDatasets, OperationChoices, \
    ModelConfigs, TrainingParameters


class ExperimentCoordinator:

    def __init__(self):
        self.experiment_sdk = ExperimentSDK()


    def run_simple_experiment(self):
        """Run a simple experiment."""
        transformation_options = DataTransformationOptions(
            z_normalize=OperationChoices.always,
            log=OperationChoices.always,
            difference=OperationChoices.always,
        )
        data_loader_parameters = DataLoaderParameters(
            dataset=AvailableDatasets.averaged_across_states,
            transformation_options=transformation_options
        )
        model_config = ModelConfigs(
            chosen_model=AvailableModelsModelConfigs.var,
            hyperparameters=VARHyperparameters(p=2)
        )
        training_parameters = TrainingParameters(
            train_percentage=0.8
        )
        experiment_config = ExperimentConfig(
            model_config=model_config,
            data_loader_parameters=data_loader_parameters,
            training_parameters=training_parameters
        )
        self.experiment_sdk.execute_experiment(experiment_config)

    def run_simple_sweep(self):
        """Run a simple hyperparameter sweep."""
        transformation_options = DataTransformationOptions(
            z_normalize=OperationChoices.always,
            log=OperationChoices.always,
            difference=OperationChoices.always,
        )
        data_loader_parameters = DataLoaderParameters(
            dataset=AvailableDatasets.averaged_across_states,
            transformation_options=transformation_options
        )
        model_config = ModelConfigs(
            chosen_model=AvailableModelsModelConfigs.varmax,
            hyperparameters=VARMAXHyperparameters(p=SweepConfig(min=1,max=6,samples=6, default=2),q=SweepConfig(min=1,max=6,samples=6, default=2))
        )
        training_parameters = TrainingParameters(
            train_percentage=0.8
        )
        experiment_config = ExperimentConfig(
            ml_model_config=model_config,
            data_loader_parameters=data_loader_parameters,
            training_parameters=training_parameters
        )
        performance_result = self.experiment_sdk.execute_sweep(experiment_config)
        print("done")

    def get_all_possible_experiments(self):
        """Get all possible experiments."""
        print("think more here")


if __name__ == '__main__':
    experiment_coordinator = ExperimentCoordinator()
    experiment_coordinator.get_all_possible_experiments()
