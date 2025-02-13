"""Main file for working with experiments."""

import os
from typing import Optional, List

import snowflake.connector
import pandas as pd
from statsmodels.tsa.stattools import adfuller
import numpy as np

from pydantic import BaseModel, ConfigDict



class RestorativeValues(BaseModel):

    model_config = ConfigDict(arbitrary_types_allowed=True)
    first_row: pd.Series
    operation_rules_list: list
    years_column: pd.Series
    state_column: Optional[pd.Series] = None
    column_order: List[str]
    dropped_columns: pd.DataFrame

class DataTransformer:
    """Main class for working with experiments."""

    def __init__(self):
        """Initialize the class."""
        self.restorative_values = None

    def base_undo_transformation(self, transformed_df):
        restored_df = {}

        # Ensure we iterate columns in the same order
        for idx, col in enumerate(transformed_df.columns):
            rules = self.restorative_values.operation_rules_list[idx]
            data = transformed_df[col].copy()

            # 1) Un-standardize: x = x_std * std + mean
            data = data * rules["std"] + rules["mean"]

            # 2) If we differenced, undo by cumulative sum and add the first value
            if rules["needs_diff"]:
                data = data.cumsum() + rules["first_value_diff"]

            # 3) If log transform was applied, exponentiate
            if rules["log"]:
                data = np.exp(data)
            restored_df[col] = data
        restored_df = pd.DataFrame(restored_df)
        return restored_df


    def undo_transformations(self,  transformed_df, add_first_row=True):
        """
        Revert the transformations (un-standardize, un-diff, un-log).

        Parameters
        ----------
        transformed_df : pd.DataFrame
            The DataFrame in the transformed space.
        operation_rules_list : list of dict
            Transformation info for each column, in the same column order as transformed_df.

        Returns
        -------
        restored_df : pd.DataFrame
            DataFrame with original-scale values restored (or as close as possible if differenced).

        operation_rules_list, first_row

        """
        restored_df = self.base_undo_transformation(transformed_df)

        if add_first_row:
            # insert the first_row[restored_df.columns] to the first row of the restored_df
            restored_df.loc[-1] = self.restorative_values.first_row[restored_df.columns]
            # correct the row order and index
            restored_df.index = restored_df.index + 1
            restored_df = restored_df.sort_index()
            # drop index and reset index
            restored_df = restored_df.reset_index(drop=True)
        restored_df["YEAR"] = self.restorative_values.years_column
        if self.restorative_values.state_column:
            restored_df["STATE_NAME"] = self.restorative_values.state_column
        restored_df = pd.concat([restored_df, self.restorative_values.dropped_columns], axis=1)
        return restored_df[self.restorative_values.column_order]

    def normalize_data(self, df, always_diff=False):
        """
        Determine and apply transformations (log, diff, standardize) for each numeric column.

        Returns
        -------
        transformed_df : pd.DataFrame
            The DataFrame after all transformations.
        operation_rules_list : list of dict
            Each dictionary has the information needed to invert the transform for that column.
            Order matches the columns in transformed_df.columns.
        """

        original_length = len(df)
        original_column_names = list(df.columns)
        numique = df.nunique()
        dropped_columns = df.loc[:, numique <= original_length//2]
        df = df.loc[:, numique > original_length//2]

        transformed_columns = []
        operation_rules_list = []
        transformed_col_names = []

        # Decide which columns to transform (e.g., skip year/state name, etc.)
        # We'll skip any non-numeric columns for clarity.
        columns_to_include = [col for col in df.columns if col not in ["YEAR", "STATE_NAME"]]
        for col in columns_to_include:

            # df[col] = df[col].astype(float)

            # Grab the original data for this column
            series = df[col].copy()

            # Prepare a dictionary to store transformation info
            rules = {
                "log": False,
                "needs_diff": False,
                "first_value_diff": None,  # We'll store the first data point after log if we do differencing
                "mean": 0.0,
                "std": 1.0
            }

            # 1) Decide on log transform based on skew
            skew_val = series.skew()
            # Example criterion: if skew > 1, do log transform
            if skew_val > 1:
                rules["log"] = True
                # You must ensure all values are > 0 for log. If your data can be zero or negative,
                # you'll need a shift, e.g.: series = np.log(series - series.min() + 1)
                try:
                    series = np.log(series)
                except Exception as err:
                    print("think")

            # 2) Check stationarity and possibly difference
            result = adfuller(series.dropna())  # dropna to avoid issues if log created NaNs
            p_value = result[1]
            if p_value > 0.05 or always_diff:
                rules["needs_diff"] = True
                # Store first value in the CURRENT scale (already log-transformed if log was True).
                rules["first_value_diff"] = series.iloc[0]
                # Perform differencing, dropping the first NaN that results
                series = series.diff().dropna()

            # 3) Standardize: subtract mean, divide by std
            mean_val = series.mean()
            std_val = series.std() if series.std() != 0 else 1.0  # avoid division by zero
            rules["mean"] = mean_val
            rules["std"] = std_val
            series = (series - mean_val) / std_val

            if len(series) == original_length:
                series = series[1:]

            # Add to our list of transformed columns
            transformed_columns.append(series)
            operation_rules_list.append(rules)
            transformed_col_names.append(col)

        first_row = df.iloc[0]
        # Combine all transformed Series into a single DataFrame
        transformed_df = pd.concat(transformed_columns, axis=1)
        # transformed_df = transformed_df[1:]
        transformed_df.columns = transformed_col_names
        self.restorative_values = RestorativeValues(
            first_row=first_row,
            operation_rules_list=operation_rules_list,
            years_column=df["YEAR"],
            column_order=original_column_names,
            dropped_columns=dropped_columns
        )
        return transformed_df

    def undo_transformation_for_forcast(self, forecast, selected_columns, correct_col_order):
        forcasted_values = pd.DataFrame(forecast, columns=selected_columns)
        forcasted_values = forcasted_values[correct_col_order]
        forcasted_values.reset_index(drop=True, inplace=True)
        corrected_forcasted_values = self.undo_transformations(forcasted_values, add_first_row=False)
        return corrected_forcasted_values
