"""Parameters to set for running an arbitrary experiment."""

from pydantic import BaseModel, ConfigDict
from enum import Enum
from typing import Optional, List, Union

from experiments.experiment_sdk_v2.ml_models.parent_ml_model_template import ParentMLModelTemplate, MLHyperparametersTemplate
from experiments.experiment_sdk_v2.ml_models.var import VARMLModelContainer, VARHyperparameters
from experiments.experiment_sdk_v2.ml_models.varmax import VARMAXMLModelContainer, VARMAXHyperparameters
from experiments.experiment_sdk_v2.submodels.data_loader import DataLoader
from experiments.experiment_sdk_v2.submodels.sweep_iterators import SweepConfig, sweep_iterator


class MLModelConfig(BaseModel):
    """Options for the model."""
    model_config = ConfigDict(arbitrary_types_allowed=True)
    ml_model_name: str
    ml_model: ParentMLModelTemplate
    ml_model_hyperparameters: MLHyperparametersTemplate

model_options = [
    MLModelConfig(
        ml_model_name="var",
        ml_model=VARMLModelContainer,
        ml_model_hyperparameters=VARHyperparameters
    ),
    MLModelConfig(
        ml_model_name="varmax",
        ml_model=VARMAXMLModelContainer,
        ml_model_hyperparameters=VARMAXHyperparameters
    )
]

data_loader = DataLoader()

class DatabaseConfig(BaseModel):
    """Options for the database."""

    database_name: str
    retriever_function: callable

available_datasets = [
    DatabaseConfig(
        database_name="averaged_across_states",
        retriever_function=data_loader.get_database_averaged_across_state
    ),
    DatabaseConfig(
        database_name="full_database",
        retriever_function=data_loader.get_full_database
    )
]


class DataAugmentations:
    """Options for data augmentations."""

    z_normalize: bool = True
    log: bool = True
    difference: bool = True
    drop_near_constant_columns: bool = True

    def get_all_sweeps(self):
        """Get all possible instantiations of the hyperparameters."""
        parameter_set = []
        z_normalize = SweepConfig(type='bool')
        log = SweepConfig(type='bool')
        difference = SweepConfig(type='bool')
        drop_near_constant_columns = SweepConfig(type='bool')
        combinations_dataframe = sweep_iterator.make_multi_parameter_search([z_normalize, log, difference, drop_near_constant_columns])
        for index, row in combinations_dataframe.iterrows():
            parameter_set.append(DataAugmentations(z_normalize=row['z_normalize'], log=row['log'], difference=row['difference'], drop_near_constant_columns=row['drop_near_constant_columns']))
        return parameter_set

class AvailableDatasets(str, Enum):
    """Available datasets for the experiment."""

    averaged_across_states = "averaged_across_states"
    full_database = "full_database"


class DatasetSubsetOptions(BaseModel):
    """Options for subset of data to request."""

    specific_states: Optional[List[str]] = None
    random_sample_n_states: Optional[int] = None

class AlwaysOrNeverOperationChoices(str, Enum):
    """Choices for the operation."""

    always = "always"
    never = "never"

class OperationChoices(str, Enum):
    """Choices for the operation."""

    always = "always"
    never = "never"
    conditional = "conditional"


class DataTransformationOptions(BaseModel):
    """Options for transforming the data."""

    z_normalize: OperationChoices = "always"
    log: OperationChoices = "always"
    difference: OperationChoices = "always"
    drop_near_constant_columns: AlwaysOrNeverOperationChoices = "always"


class DataLoaderParameters(BaseModel):
    """Parameters for the data loader."""

    dataset: AvailableDatasets
    subset_options: Optional[DatasetSubsetOptions] = None
    transformation_options: DataTransformationOptions



class AvailableModelsModelConfigs(str, Enum):
    """Choices for the base model."""

    var = "var"
    varmax = "varmax"

class ModelConfigs(BaseModel):
    """Choices for the model."""

    chosen_model: AvailableModelsModelConfigs
    hyperparameters: Union[VARHyperparameters,VARMAXHyperparameters]

class TrainingParameters(BaseModel):
    """Parameters for training the model."""

    train_percentage: float
    loss_metric: str = "mse"

class ExperimentConfig(BaseModel):
    """Parameters for the experiment."""

    ml_model_config: ModelConfigs
    data_loader_parameters: DataLoaderParameters
    training_parameters: TrainingParameters


def get_all_possible_experiment_configs():
    """Get all possible experiment configurations."""
    pass

if __name__ == '__main__':
    cow = DataAugmentations()
    out = cow.get_all_sweeps()
    print("think more here")

