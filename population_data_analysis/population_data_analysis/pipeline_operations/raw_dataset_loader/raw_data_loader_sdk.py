"""Data loader sdk."""

from cachetools import LRUCache, cached

from population_data_analysis.pipeline_operations.raw_dataset_loader.raw_data_loader_config_objects import (
    AvailableDataRetrivalOperations,
    RetrivalParameters,
)
from population_data_analysis.pipeline_operations.raw_dataset_loader.raw_data_loader_modules.raw_data_loader import (
    RawDataLoader,
)

cache = LRUCache(maxsize=100)


class RawDataLoaderSDK:
    """Data loader sdk."""

    def __init__(self):
        """Initialize the class."""
        self.data_loader = RawDataLoader()

    @cached(cache)
    def run(
        self,
        retrival_parameters: RetrivalParameters,
        operation: AvailableDataRetrivalOperations,
    ):
        """Run the data loader."""
        if operation == AvailableDataRetrivalOperations.averaged_across_states:
            return self.data_loader.get_database_averaged_across_state(
                retrival_parameters
            )
        if operation == AvailableDataRetrivalOperations.full_database:
            return self.data_loader.get_full_database(retrival_parameters)
        raise ValueError("Invalid operation.")
