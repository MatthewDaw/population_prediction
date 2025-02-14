"""Configuration objects for the ML models."""

from enum import Enum
from typing import Literal, Union

from population_data_analysis.common import BasePydanticForRepo


class AvailableMLOperations(str, Enum):
    """Available data retrival operations."""

    var = "var"
    varmax = "varmax"


class VARHyperparameters(BasePydanticForRepo):
    """Hyperparameters for the VAR model."""

    p: int = 1


class VARMAXHyperparameters(BasePydanticForRepo):
    """Hyperparameters for the VARMAX model."""

    p: int = 1
    q: int = 1
    trend: Union[Literal["c"], Literal["trend"]] = "c"
