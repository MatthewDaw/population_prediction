"""Evaluation config objects."""

from enum import Enum
from typing import List, Optional

from population_data_analysis.common import BasePydanticForRepo


class AvailableEvaluationOperations(str, Enum):
    """Available data retrival operations."""

    evaluate_model = "evaluate_model"


class EvaluationConfig(BasePydanticForRepo):
    """Parameters for retrieving data."""

    metrics: Optional[List[str]] = ["mse", "mae"]


class EvaluationOutput(BasePydanticForRepo):
    """Evaluation output."""

    mse: Optional[float] = None
    mae: Optional[float] = None
    failed: Optional[bool] = (False,)
    error_message: Optional[str] = (None,)

    def __str__(self):
        if self.failed:
            return f"Failed with error: {self.error_message}"
        return f"Mean squared error: {self.mse}, Mean absolute error: {self.mae}"
