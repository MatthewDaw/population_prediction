"""Simple function for retrieving a model."""
from experiments.experiment_sdk_v2.ml_models.var import VARMLModelContainer
from experiments.experiment_sdk_v2.ml_models.varmax import VARMAXMLModelContainer
from experiments.experiment_sdk_v2.submodels.experiment_parameters import ModelConfigs, AvailableModelsModelConfigs


def retrieve_model(model_config: ModelConfigs):
    """Retrieve a model."""

    if model_config.chosen_model == AvailableModelsModelConfigs.var:
        return VARMLModelContainer(model_config.hyperparameters)

    if model_config.chosen_model == AvailableModelsModelConfigs.varmax:
        return VARMAXMLModelContainer(model_config.hyperparameters)
