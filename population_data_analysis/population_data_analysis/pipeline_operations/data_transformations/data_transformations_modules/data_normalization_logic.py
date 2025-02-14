"""Data normalization logic for the data transformation pipeline."""

import numpy as np
import pandas as pd
from statsmodels.tsa.stattools import adfuller


def drop_near_constant(
    df: pd.DataFrame, min_unique_ratio: float = 0.5
) -> (pd.DataFrame, pd.DataFrame):
    """Drop columns with too few unique values."""
    nunique = df.nunique()
    keep = nunique > (len(df) * min_unique_ratio)
    dropped = df.loc[:, ~keep]
    return df.loc[:, keep], dropped


def apply_log(series: pd.Series, option: str) -> (pd.Series, dict):
    """Apply log transform if forced or if skew > 1 (when conditional)."""
    rules = {"log": False}
    if option == "always" or (option == "conditional" and series.skew() > 1):
        rules["log"] = True
        # shift if necessary
        if (series <= 0).any():
            shift = abs(series.min()) + 1
            rules["log_shift"] = shift
            series = np.log(series + shift)
        else:
            series = np.log(series)
    return series, rules


def apply_difference(series: pd.Series, option: str) -> (pd.Series, dict):
    """Difference the series if forced or if non-stationary (p-value > 0.05)."""
    rules = {"needs_diff": False, "first_value_diff": None}
    result = adfuller(series.dropna())
    p_value = result[1]
    if option == "always" or (option == "conditional" and p_value > 0.05):
        rules["needs_diff"] = True
        rules["first_value_diff"] = series.iloc[0]
        series = series.diff().dropna()
    return series, rules


def standardize_series(series: pd.Series, option: str) -> (pd.Series, dict):
    """Z-normalize the series if requested."""
    rules = {"mean": 0.0, "std": 1.0}
    if option == "always":
        mean_val = series.mean()
        std_val = series.std() if series.std() != 0 else 1.0
        rules["mean"] = mean_val
        rules["std"] = std_val
        series = (series - mean_val) / std_val
    return series, rules


def drop_highly_correlated(df: pd.DataFrame, threshold: float) -> (pd.DataFrame, list):
    """Drop one of each pair of columns that are highly correlated."""
    corr_matrix = df.corr().abs()
    upper = corr_matrix.where(np.triu(np.ones(corr_matrix.shape), k=1).astype(bool))
    to_drop = [col for col in upper.columns if any(upper[col] > threshold)]
    return df.drop(columns=to_drop), to_drop


def add_jitter(df: pd.DataFrame, jitter: float) -> pd.DataFrame:
    """Add small noise to break perfect collinearity."""
    if jitter > 0:
        noise = np.random.normal(0, jitter, size=df.shape)
        return df + noise
    return df


# The simplified DataTransformer class:
class DataTransformer:
    """Simplified data transformer using helper functions."""

    def __init__(self):
        self.restorative_values = None

    def normalize_data(
        self, df: pd.DataFrame, options: "DataTransformationOptions"
    ) -> pd.DataFrame:
        """Normalize the data using the provided options."""

        original_length = len(df)
        original_cols = list(df.columns)

        # Step 0: Drop near-constant columns if requested
        if options.drop_near_constant_columns == "always":
            df, dropped = drop_near_constant(df, min_unique_ratio=0.5)
        else:
            dropped = pd.DataFrame()

        rules_list = {}
        transformed_cols = {}

        # Process each numeric column (skip identifiers)
        for col in df.columns:
            if col in ["YEAR", "STATE_NAME"]:
                continue
            if not pd.api.types.is_numeric_dtype(df[col]):
                continue

            series = df[col].copy()
            col_rules = {}

            # 1. Log transform
            series, log_rules = apply_log(series, options.log)
            col_rules.update(log_rules)

            # 2. Difference the series
            series, diff_rules = apply_difference(series, options.difference)
            col_rules.update(diff_rules)

            # 3. Standardize
            series, std_rules = standardize_series(series, options.z_normalize)
            col_rules.update(std_rules)

            # Align length if differencing dropped first element
            if len(series) == original_length:
                series = series[1:]
            transformed_cols[col] = series
            rules_list[col] = col_rules

        transformed_df = pd.DataFrame(transformed_cols)

        # 4. Optionally drop highly correlated columns
        if options.drop_correlated_columns == "always":
            transformed_df, dropped_corr = drop_highly_correlated(
                transformed_df, options.correlation_threshold
            )
            for col in rules_list:  # pylint: disable=consider-using-dict-items
                rules_list[col]["dropped_due_to_correlation"] = dropped_corr

        # 5. Optionally add jitter
        transformed_df = add_jitter(transformed_df, options.jitter)

        # Store restorative values for undoing the transforms later.
        first_row = df.iloc[0]
        self.restorative_values = {
            "first_row": first_row,
            "operation_rules": rules_list,
            "years_column": df["YEAR"] if "YEAR" in df.columns else None,
            "dropped_columns": dropped,
            "column_order": original_cols,
            "remaining_columns": list(transformed_df.columns),
        }
        return transformed_df
