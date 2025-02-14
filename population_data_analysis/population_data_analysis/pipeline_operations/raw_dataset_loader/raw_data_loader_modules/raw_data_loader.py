"""Get all possible run configurations for all sweep experiments."""

import os

import pandas as pd
import snowflake.connector

from population_data_analysis.pipeline_operations.raw_dataset_loader.raw_data_loader_config_objects import (
    AvailableDataRetrivalOperations,
    RetrivalParameters,
)


class RawDataLoader:
    """Class for loading raw data."""

    def run_query(self, query):
        """Run a query."""

        # Define connection parameters
        conn = snowflake.connector.connect(
            user=os.getenv("dbt_user"),
            password=os.getenv("dbt_password"),
            account=os.getenv("dbt_account"),
            warehouse="COMPUTE_WH",
            database="POP_PREDICTION",
            schema="DEV",  # Change to "dev" if needed
            role="transform",
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

    def standardize_data_types(self, df: pd.DataFrame) -> pd.DataFrame:
        """Standardize the data types."""
        for col in df.columns:
            if col not in ["YEAR", "STATE_NAME"]:
                df[col] = df[col].astype(float)
        return df

    def get_database_averaged_across_state(
        self, retrival_parameters: RetrivalParameters
    ):
        """Get the database averaged across the state."""
        del retrival_parameters
        # retrival paramters are just passed in so that template works
        query = "select * from POP_PREDICTION.DEV.pop_prediction_training_avg_across_state order by year"
        raw_data = self.run_query(query)
        raw_data = self.standardize_data_types(raw_data)
        return raw_data

    def get_full_database(self, subset_options: RetrivalParameters):
        """Get the full database."""
        if subset_options.specific_states:
            query = f"select * from POP_PREDICTION.DEV.POP_PREDICTION_TRAINING where state_name in {tuple(subset_options.specific_states)} order by year, state_name"
        elif subset_options.random_sample_n_states:
            # query to get full list of all available states
            query = "select distinct state_name from POP_PREDICTION.DEV.POP_PREDICTION_TRAINING"
            df = self.run_query(query)
            # get random sample of n states
            states = df.sample(
                n=subset_options.random_sample_n_states
            ).STATE_NAME.tolist()
            if len(states) == 1:
                query = f"select * from POP_PREDICTION.DEV.POP_PREDICTION_TRAINING where state_name = '{states[0]}' order by year, state_name"
            else:
                query = f"select * from POP_PREDICTION.DEV.POP_PREDICTION_TRAINING where state_name in {tuple(states)} order by year, state_name"
        else:
            query = "select * from POP_PREDICTION.DEV.POP_PREDICTION_TRAINING order by year, state_name "

        df = self.run_query(query)

        if (
            subset_options.random_sample_n_states is not None
            and subset_options.random_sample_n_states == 1
        ) or (
            subset_options.specific_states is not None
            and len(subset_options.specific_states) == 1
        ):
            df_final = self.standardize_data_types(df)
            return df_final

        df_pivoted = df.pivot(
            index="YEAR",
            columns="STATE_NAME",
            values=[el for el in df.columns if el not in ("STATE_NAME", "YEAR")],
        )
        df_pivoted.columns = [f"{state}/{col}" for col, state in df_pivoted.columns]
        df_final = df_pivoted.reset_index(drop=False)
        df_final = self.standardize_data_types(df_final)
        return df_final

    def function_forwarder(
        self,
        chosen_function: AvailableDataRetrivalOperations,
        retrival_parameters: RetrivalParameters,
    ):
        """Forward the function."""
        if chosen_function == AvailableDataRetrivalOperations.averaged_across_states:
            return self.get_database_averaged_across_state(retrival_parameters)
        if chosen_function == AvailableDataRetrivalOperations.full_database:
            return self.get_full_database(retrival_parameters)
        raise ValueError("Invalid operation")
