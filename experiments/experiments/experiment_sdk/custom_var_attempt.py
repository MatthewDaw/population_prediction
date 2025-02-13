"""Model for making custom VAR model."""

import pandas as pd
import numpy as np
from scipy.linalg import lstsq

class CustomVAR:
    """Model for making custom VAR model."""

    def __init__(self, df: pd.DataFrame, state_name_to_column_names: dict):
        """Initialize the class."""
        self.df = df
        self.state_name_to_column_names = state_name_to_column_names
        self.coefs_ = None

    def fit_for_specific_state(self, df: pd.DataFrame, p: int):
        """Fit the model for a specific state."""
        T = df.shape[0] # Number of observations
        n = df.shape[1]  # Number of time series

        Y = df.values[p:]  # shape = (T-p, n)

        # Construct X by stacking the lagged values
        X_list = []
        for t in range(p, T):
            # Intercept
            row = [1.0]
            # Append p lags
            for lag in range(1, p + 1):
                row.extend(df.values[t - lag])
            X_list.append(row)

        X = np.array(X_list)  # shape = (T-p, 1 + n*p)

        self.coefs_, residuals, rank, s = lstsq(X, Y)
        print("think more here")


    def fit(self, p: int):
        """Fit the model."""
        for state_name, columns_for_state in self.state_name_to_column_names.items():
            self.fit_for_specific_state(self.df[columns_for_state], p)
        print("think here")




