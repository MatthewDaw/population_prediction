"""Config objects for data transformation operations."""

from enum import Enum
from typing import List, Optional

import pandas as pd
from pydantic import BaseModel

from population_data_analysis.common import BasePydanticForRepo


class RestorativeValues(BasePydanticForRepo):
    """Values needed to restore the original data from transformed data."""

    first_row: pd.Series
    operation_rules_list: list
    years_column: pd.Series
    state_column: Optional[pd.Series] = None
    column_order: List[str]
    dropped_columns: pd.DataFrame
    remaining_column_names: List[str]


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
    train_test_split: float = 0.8

    # New options to help with singularity issues
    drop_correlated_columns: AlwaysOrNeverOperationChoices = "always"
    correlation_threshold: float = 0.99  # drop one column if |corr| > threshold
    jitter: float = 0.01  # e.g. 0.01 will add small noise


class AvailableDataTransformationOperations(str, Enum):
    """Available data transformation operations."""

    data_transformation = "data_transformation"
