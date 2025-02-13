"""Data loader for experiments sdk."""

import os
from typing import List

import snowflake.connector
import pandas as pd
from pandas.testing import assert_frame_equal

from experiments.experiment_sdk_v2.submodels.data_normalizer import DataTransformer
from experiments.experiment_sdk_v2.submodels.experiment_parameters import DataLoaderParameters, AvailableDatasets, \
    DatasetSubsetOptions


class DataLoader:
    """Class for loading tools and techniques for experimenting with data."""

    def __init__(self):
        self.data_transformer = DataTransformer()

    def standardize_data_types(self, df):
        """Standardize the data types."""
        for col in df.columns:
            if col not in ['YEAR', 'STATE_NAME']:
                df[col] = df[col].astype(float)
        return df

    def run_query(self, query):
        # Define connection parameters
        conn = snowflake.connector.connect(
            user=os.getenv("dbt_user"),
            password=os.getenv("dbt_password"),
            account=os.getenv("dbt_account"),
            warehouse="COMPUTE_WH",
            database="POP_PREDICTION",
            schema="DEV",  # Change to "dev" if needed
            role="transform"
        )

        # Create a cursor object
        cur = conn.cursor()

        # Execute a query
        cur.execute(query)

        # Fetch all results into a pandas DataFrame
        df = pd.DataFrame(cur.fetchall(), columns=[desc[0] for desc in cur.description])

        # Close the cursor and connection
        cur.close()
        conn.close()

        return df

    def get_database_averaged_across_state(self):
        """Get the database averaged across the state."""
        query = "select * from POP_PREDICTION.DEV.pop_prediction_training_avg_across_state order by year"
        raw_data = self.run_query(query)
        raw_data = self.standardize_data_types(raw_data)
        return raw_data

    def get_full_database(self, subset_options: DatasetSubsetOptions):
        """Get the full database."""
        if subset_options.specific_states:
            query = f"select * from POP_PREDICTION.DEV.POP_PREDICTION_TRAINING where state_name in {tuple(subset_options.specific_states)} order by year, state_name"
        elif subset_options.random_sample_n_states:
            # query to get full list of all available states
            query = f"select distinct state_name from POP_PREDICTION.DEV.POP_PREDICTION_TRAINING"
            df = self.run_query(query)
            # get random sample of n states
            states = df.sample(n=subset_options.random_sample_n_states).state_name.tolist()
            query = f"select * from POP_PREDICTION.DEV.POP_PREDICTION_TRAINING where state_name in {tuple(states)} order by year, state_name"
        else:
            query = "select * from POP_PREDICTION.DEV.POP_PREDICTION_TRAINING order by year, state_name "

        df = self.run_query(query)

        if subset_options.random_sample_n_states == 1 or len(subset_options.specific_states) == 1:
            df_final = self.standardize_data_types(df)
            return df_final

        df_pivoted = df.pivot(
            index="YEAR",
            columns="STATE_NAME",
            values=[el for el in df.columns if el != 'STATE_NAME' and el !='YEAR']
        )
        df_pivoted.columns = [
            f"{state}/{col}"
            for col, state in df_pivoted.columns
        ]
        df_final = df_pivoted.reset_index(drop=False)
        transformed_data = self.data_transformer.normalize_data(df_final)
        return df_final, transformed_data

    def dataframes_almost_equal(self, df1: pd.DataFrame, df2: pd.DataFrame, tol=1e-6) -> bool:
        """
        Return True if df1 and df2 are equal within `tol`, otherwise False. Used for testing undoing transformations.
        """
        try:
            # By default, check 'exact' matches except for the given tolerance
            assert_frame_equal(df1, df2, atol=tol)
            return True
        except AssertionError:
            return False

    def _get_raw_data(self, requested_dataset: AvailableDatasets, subset_options: DatasetSubsetOptions =None):
        """Get the raw data."""
        if requested_dataset == AvailableDatasets.averaged_across_states:
            return self.get_database_averaged_across_state()
        elif requested_dataset == AvailableDatasets.full_database:
            return self.get_full_database(subset_options)

    def get_dataset(self, data_loader_parameters: DataLoaderParameters):
        """Get the data requested by data load parameters."""
        raw_data = self._get_raw_data(data_loader_parameters.dataset, data_loader_parameters.subset_options)
        normalized_data = self.data_transformer.normalize_data(raw_data, data_loader_parameters.transformation_options)
        return raw_data, normalized_data


