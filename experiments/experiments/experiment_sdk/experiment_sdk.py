"""Main file for working with experiments."""

import os
from collections import defaultdict
from typing import List, Optional

import numpy as np
import pandas as pd
import snowflake.connector
from pandas.testing import assert_frame_equal, assert_series_equal
from pydantic import BaseModel, ConfigDict
from statsmodels.tsa.stattools import adfuller

from experiments.experiment_sdk.analysis_engine import VARModelOptimizer
from experiments.experiment_sdk.custom_var_attempt import CustomVAR
from experiments.experiment_sdk.data_normalizer import DataTransformer
from experiments.experiment_sdk.visualizor import Visualizer


class RestorativeValues(BaseModel):

    model_config = ConfigDict(arbitrary_types_allowed=True)
    first_row: pd.Series
    operation_rules_list: list
    years_column: pd.Series
    state_column: Optional[pd.Series] = None
    column_order: List[str]


class ExperimentSDK:
    """Main class for working with experiments."""

    def __init__(self):
        """Initialize the class."""
        self.data_transformation = DataTransformer()
        self.visualizer = Visualizer()

    def run_query(self, query):
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

    def standardize_data_types(self, df):
        """Standardize the data types."""
        for col in df.columns:
            if col not in ["YEAR", "STATE_NAME"]:
                df[col] = df[col].astype(float)
        return df

    def get_database_averaged_across_state(self):
        """Get the database averaged across the state."""
        query = "select * from POP_PREDICTION.DEV.pop_prediction_training_avg_across_state order by year"
        return self.standardize_data_types(self.run_query(query))

    def get_full_database(self):
        """Get the full database."""
        query = "select * from POP_PREDICTION.DEV.POP_PREDICTION_TRAINING order by year, state_name "
        df = self.run_query(query)

        df_pivoted = df.pivot(
            index="YEAR",
            columns="STATE_NAME",
            values=[el for el in df.columns if el != "STATE_NAME" and el != "YEAR"],
        )

        # 3) Flatten the multi-level columns
        df_pivoted.columns = [f"{state}/{col}" for col, state in df_pivoted.columns]

        # 4) Now, df_pivoted has "index" as its index. If you prefer, make "index" a column:
        df_final = df_pivoted.reset_index(drop=False)
        return self.standardize_data_types(df_final)

    import pandas as pd
    from pandas.testing import assert_frame_equal

    def frames_almost_equal(
        self, df1: pd.DataFrame, df2: pd.DataFrame, tol=1e-6
    ) -> bool:
        """
        Return True if df1 and df2 are equal within `tol`, otherwise False.
        """
        try:
            # By default, check 'exact' matches except for the given tolerance
            assert_frame_equal(df1, df2, atol=tol)
            return True
        except AssertionError:
            return False

    def attempt_custom_var(self):
        pass

    def run_grouped_simulation(self, visualize=False):
        """Run the experiment."""
        dataset = self.get_database_averaged_across_state()
        normalized_dataset = self.data_transformation.normalize_data(dataset, True)
        normalized_dataset_reserve = normalized_dataset.copy()
        analysis_engine = VARModelOptimizer(normalized_dataset)
        selected_columns, best_hyperparams, performance = analysis_engine.run()

        if visualize:
            corrected_forcasted_values = (
                self.data_transformation.undo_transformation_for_forcast(
                    performance["forecast"],
                    selected_columns,
                    normalized_dataset_reserve.columns,
                )
            )
            self.visualizer.plot_true_and_predictions(
                dataset, corrected_forcasted_values
            )

    def run_custom_var_model(self):
        dataset = self.get_full_database()
        normalized_dataset = self.data_transformation.normalize_data(dataset, True)
        state_name_to_column_names = defaultdict(list)
        for col in normalized_dataset.columns:
            state_name_to_column_names[col.split("/")[1]].append(col)
        custom_var = CustomVAR(normalized_dataset, state_name_to_column_names)
        custom_var.fit(p=3)


if __name__ == "__main__":
    experiment_sdk = ExperimentSDK()
    experiment_sdk.run_grouped_simulation()
