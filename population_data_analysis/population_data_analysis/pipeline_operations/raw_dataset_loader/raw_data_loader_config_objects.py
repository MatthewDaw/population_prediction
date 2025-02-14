"""Raw data loader configuration objects."""

from enum import Enum
from typing import List, Optional

from population_data_analysis.common import BasePydanticForRepo


class AvailableDataRetrivalOperations(str, Enum):
    """Available data retrival operations."""

    averaged_across_states = "averaged_across_states"
    full_database = "full_database"


class RetrivalParameters(BasePydanticForRepo):
    """Parameters for retrieving data."""

    specific_states: Optional[List[str]] = None
    random_sample_n_states: Optional[int] = None
