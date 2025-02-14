"""Data transformations sdk."""

import pandas as pd

from population_data_analysis.pipeline_operations.data_transformations.data_transformation_config_objects import (
    DataTransformationOptions,
)
from population_data_analysis.pipeline_operations.data_transformations.data_transformations_modules.data_normalization_logic import (
    DataTransformer,
)


class DataTransformationsSDK:
    """Data transformations sdk."""

    def __init__(self):
        """Initialize the class."""
        self.data_transformer = DataTransformer()

    def run(self, data: pd.DataFrame, options: DataTransformationOptions):
        """Run the data transformations."""
        # data = data.drop(columns=['STATE','YEAR'], errors='ignore')
        try:
            normalized_data = self.data_transformer.normalize_data(data, options)
        except Exception as e:  # pylint: disable=broad-exception-caught
            print(f"Error in data transformation: {e}")
            self.data_transformer.normalize_data(data, options)
            return None, None
        train_test_split = options.train_test_split
        break_point = int(len(normalized_data) * train_test_split)
        train_data = normalized_data[:break_point]
        test_data = normalized_data[break_point:]
        return train_data, test_data
