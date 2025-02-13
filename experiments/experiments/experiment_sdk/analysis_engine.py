import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.api import VAR
from sklearn.metrics import mean_squared_error, mean_absolute_error
from sklearn.feature_selection import mutual_info_regression
from statsmodels.tsa.statespace.sarimax import SARIMAX


class VARModelOptimizer:
    """
    A class to optimize column selection and hyperparameters for several model types
    on a multivariate time series DataFrame. The DataFrame is assumed to have been logged
    and differenced.

    Supported models:
      - 'VAR'      : Multivariate Vector Autoregression.
      - 'VARMAX'   : Multivariate VARMAX (with MA order fixed to 0).
      - 'SARIMAX'  : Fits a univariate SARIMAX model (order=(p,0,0)) on each selected column.
      - 'MARKOV'   : Fits a univariate Markov Autoregression model on each selected column.

    Key functionalities:
      - Column Selection: Selects the top n columns using correlation or mutual information.
      - Hyperparameter Optimization: Grid searches over the lag (or AR) order (p) for the chosen model.
      - Model Fitting & Evaluation: Splits the data into train/validation/test sets,
        fits the selected model, and reports forecasting performance (e.g., MSE or MAE).

    Example usage:

        import pandas as pd
        from VARModelOptimizer import VARModelOptimizer

        # Assume df is your preprocessed DataFrame
        optimizer = VARModelOptimizer(df, model_type='MARKOV')  # Options: 'VAR', 'VARMAX', 'SARIMAX', 'MARKOV'
        selected_columns, best_hyperparams, performance = optimizer.run(
            n_columns=3,
            selection_method='correlation',  # or 'mutual_info'
            p_range=range(1, 6),
            metric='mse'
        )
        print("Selected Columns:", selected_columns)
        print("Best Hyperparameters:", best_hyperparams)
        print("Model Performance:", performance)
    """

    def __init__(self, data: pd.DataFrame, model_type: str = 'VAR'):
        """
        Initialize the optimizer with a DataFrame and a model type.

        Parameters:
            data (pd.DataFrame): Multivariate time series data (logged & differenced).
            model_type (str): Model type to use. Options:
                              'VAR', 'VARMAX', 'SARIMAX', or 'MARKOV'.
        """
        self.data = data.copy()
        self.model_type = model_type.upper()  # Convert to uppercase for consistency.
        self.preprocessed_data = self.preprocess_data()

    def preprocess_data(self) -> pd.DataFrame:
        """
        Preprocess the data if necessary.

        Currently, this method simply returns a copy of the data.
        Returns:
            pd.DataFrame: Preprocessed data.
        """
        return self.data.copy()

    def select_columns(self, n_columns: int = None, method: str = 'correlation') -> list:
        """
        Select the top n columns based on importance scores.

        Two methods are supported:
          - 'correlation': Computes the average absolute Pearson correlation of each column with all others.
          - 'mutual_info': Computes the mutual information between each column's one-step lag and its current value.

        Parameters:
            n_columns (int): The number of top columns to select.
            method (str): 'correlation' or 'mutual_info'.

        Returns:
            list: List of selected column names.
        """
        df = self.preprocessed_data
        total_cols = df.shape[1]
        if n_columns is None or n_columns > total_cols:
            n_columns = total_cols

        scores = {}
        if method == 'correlation':
            corr_matrix = df.corr().abs()
            for col in df.columns:
                scores[col] = corr_matrix.loc[col].drop(col).mean()
        elif method == 'mutual_info':
            for col in df.columns:
                series = df[col].dropna()
                if len(series) < 2:
                    scores[col] = 0
                else:
                    X = series.shift(1).dropna().values.reshape(-1, 1)
                    y = series.iloc[1:].values
                    mi = mutual_info_regression(X, y, random_state=0)
                    scores[col] = mi[0]
        else:
            raise ValueError("Unsupported method. Use 'correlation' or 'mutual_info'.")
        sorted_cols = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        selected_columns = [col for col, score in sorted_cols[:n_columns]]
        return selected_columns

    def optimize_hyperparameters(self, selected_columns: list, p_range=range(1, 11), metric: str = 'mse') -> dict:
        """
        Optimize the model's order (p) using a grid search over the candidate range.

        Parameters:
            selected_columns (list): List of columns to use.
            p_range (iterable): Candidate orders (p values) to try.
            metric (str): 'mse' or 'mae'.

        Returns:
            dict: Dictionary containing the best hyperparameter, e.g., {'p': best_p}.
        """
        data = self.preprocessed_data[selected_columns]
        n_obs = len(data)
        train_end = int(n_obs * 0.7)
        val_end = int(n_obs * 0.85)
        train_data = data.iloc[:train_end]
        val_data = data.iloc[train_end:val_end]

        best_score = np.inf
        best_p = None

        for p in p_range:
            try:
                if self.model_type == 'VAR':
                    model = VAR(train_data)
                    model_fit = model.fit(p)
                    lag_obs = train_data.values[-p:]
                    forecast = model_fit.forecast(lag_obs, steps=len(val_data))
                elif self.model_type == 'VARMAX':
                    from statsmodels.tsa.statespace.varmax import VARMAX
                    model = VARMAX(train_data, order=(p, 0))
                    model_fit = model.fit(disp=False)
                    forecast = model_fit.forecast(steps=len(val_data))
                elif self.model_type == 'SARIMAX':
                    # Fit univariate SARIMAX models for each column and average the error.
                    errors = []
                    for col in selected_columns:
                        series_train = train_data[col]
                        series_val = val_data[col]
                        model = SARIMAX(series_train, order=(p, 0, 0))
                        model_fit = model.fit(disp=False)
                        fc = model_fit.forecast(steps=len(series_val))
                        if metric == 'mse':
                            err = mean_squared_error(series_val, fc)
                        elif metric == 'mae':
                            err = mean_absolute_error(series_val, fc)
                        else:
                            raise ValueError("Unsupported metric. Use 'mse' or 'mae'.")
                        errors.append(err)
                    error = np.mean(errors)
                    if error < best_score:
                        best_score = error
                        best_p = p
                    continue  # Move to the next candidate p.
                elif self.model_type == 'MARKOV':
                    # For Markov Autoregression, fit each column individually.
                    from statsmodels.tsa.regime_switching.markov_autoregression import MarkovAutoregression
                    errors = []
                    for col in selected_columns:
                        series_train = train_data[col]
                        series_val = val_data[col]
                        model = MarkovAutoregression(series_train, k_regimes=2, order=p, switching_ar=True)
                        model_fit = model.fit(disp=False)
                        fc = model_fit.forecast(steps=len(series_val))
                        if metric == 'mse':
                            err = mean_squared_error(series_val, fc)
                        elif metric == 'mae':
                            err = mean_absolute_error(series_val, fc)
                        else:
                            raise ValueError("Unsupported metric. Use 'mse' or 'mae'.")
                        errors.append(err)
                    error = np.mean(errors)
                    if error < best_score:
                        best_score = error
                        best_p = p
                    continue
                else:
                    raise ValueError("Unsupported model type. Use 'VAR', 'VARMAX', 'SARIMAX', or 'MARKOV'.")
            except Exception as e:
                # Skip candidate orders that cause errors.
                continue

            # For VAR and VARMAX, compute the error on the validation set.
            if self.model_type in ['VAR', 'VARMAX']:
                if metric == 'mse':
                    error = mean_squared_error(val_data.values, forecast)
                elif metric == 'mae':
                    error = mean_absolute_error(val_data.values, forecast)
                else:
                    raise ValueError("Unsupported metric. Use 'mse' or 'mae'.")
                if error < best_score:
                    best_score = error
                    best_p = p

        if best_p is None:
            raise ValueError("Failed to determine an optimal order p. Check your data and p_range.")
        return {'p': best_p}

    def evaluate_model(self, selected_columns: list, hyperparams: dict, metric: str = 'mse') -> dict:
        """
        Fit the model with the selected columns and hyperparameters on training+validation data,
        then evaluate its forecasting performance on the test set.

        Parameters:
            selected_columns (list): List of columns to use.
            hyperparams (dict): Hyperparameters for the model (e.g., {'p': best_p}).
            metric (str): 'mse' or 'mae'.

        Returns:
            dict: A dictionary with performance metrics and forecast details.
                  Example: {'metric': 'mse', 'error': 0.123, 'forecast': [...], 'test_actual': [...]}
        """
        data = self.preprocessed_data[selected_columns]
        n_obs = len(data)
        train_val_end = int(n_obs * 0.85)
        train_val_data = data.iloc[:train_val_end]
        test_data = data.iloc[train_val_end:]
        p = hyperparams.get('p', 1)

        if self.model_type == 'VAR':
            model = VAR(train_val_data)
            model_fit = model.fit(p)
            lag_obs = train_val_data.values[-p:]
            forecast = model_fit.forecast(lag_obs, steps=len(test_data))
        elif self.model_type == 'VARMAX':
            from statsmodels.tsa.statespace.varmax import VARMAX
            model = VARMAX(train_val_data, order=(p, 0))
            model_fit = model.fit(disp=False)
            forecast = model_fit.forecast(steps=len(test_data))
        elif self.model_type == 'SARIMAX':
            forecasts = []
            for col in selected_columns:
                series_train_val = train_val_data[col]
                series_test = test_data[col]
                model = SARIMAX(series_train_val, order=(p, 0, 0))
                model_fit = model.fit(disp=False)
                fc = model_fit.forecast(steps=len(series_test))
                forecasts.append(fc.values)
            forecast = np.column_stack(forecasts)
        elif self.model_type == 'MARKOV':
            from statsmodels.tsa.regime_switching.markov_autoregression import MarkovAutoregression
            forecasts = []
            for col in selected_columns:
                series_train_val = train_val_data[col]
                series_test = test_data[col]
                model = MarkovAutoregression(series_train_val, k_regimes=2, order=p, switching_ar=True)
                model_fit = model.fit(disp=False)
                fc = model_fit.forecast(steps=len(series_test))
                forecasts.append(fc)
            forecast = np.column_stack(forecasts)
        else:
            raise ValueError("Unsupported model type. Use 'VAR', 'VARMAX', 'SARIMAX', or 'MARKOV'.")

        if metric == 'mse':
            error = mean_squared_error(test_data.values, forecast)
        elif metric == 'mae':
            error = mean_absolute_error(test_data.values, forecast)
        else:
            raise ValueError("Unsupported metric. Use 'mse' or 'mae'.")

        performance = {
            'metric': metric,
            'error': error,
            'forecast': forecast,
            'test_actual': test_data.values
        }
        return performance

    def optimize_columns_and_hyperparams(self, n_columns: int = None, selection_method: str = 'correlation',
                                         p_range=range(1, 11), metric: str = 'mse') -> tuple:
        """
        Optimize both the column selection and the model hyperparameters.

        Parameters:
            n_columns (int): Number of top columns to select.
            selection_method (str): 'correlation' or 'mutual_info'.
            p_range (iterable): Candidate orders (p values) for hyperparameter optimization.
            metric (str): 'mse' or 'mae'.

        Returns:
            tuple: (selected_columns, best_hyperparameters)
        """
        selected_columns = self.select_columns(n_columns=n_columns, method=selection_method)
        best_hyperparams = self.optimize_hyperparameters(selected_columns, p_range=p_range, metric=metric)
        return selected_columns, best_hyperparams

    def run(self, n_columns: int = None, selection_method: str = 'correlation',
            p_range=range(1, 11), metric: str = 'mse') -> tuple:
        """
        Run the full optimization pipeline:
          1. Optimize column selection.
          2. Optimize model hyperparameters.
          3. Fit the model and evaluate it on the test set.

        Parameters:
            n_columns (int): Number of columns to select.
            selection_method (str): 'correlation' or 'mutual_info'.
            p_range (iterable): Candidate orders for the model.
            metric (str): 'mse' or 'mae'.

        Returns:
            tuple: (selected_columns, best_hyperparameters, performance_metrics)
        """
        selected_columns, best_hyperparams = self.optimize_columns_and_hyperparams(
            n_columns=n_columns,
            selection_method=selection_method,
            p_range=p_range,
            metric=metric
        )
        performance = self.evaluate_model(selected_columns, best_hyperparams, metric=metric)
        return selected_columns, best_hyperparams, performance


