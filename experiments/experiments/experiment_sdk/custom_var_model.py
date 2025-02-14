#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Object-Oriented VAR Model Analysis with Safe Lag Handling

This module simulates data for 50 U.S. states (each with 12 time points and 22 variables),
fits state-level VAR models (if enough degrees of freedom are available), combines data to
fit a global VAR model, analyzes the estimated coefficients to uncover significant inter-state
relationships, and visualizes the results.

Usage:
    Run this script directly. It will simulate the data, run the analysis, and produce visualizations.
"""

import warnings

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import pandas as pd
import seaborn as sns
from scipy.stats import t as t_dist
from statsmodels.tsa.api import VAR
from statsmodels.tsa.stattools import adfuller

warnings.filterwarnings("ignore")


class VARModelAnalyzer:
    def __init__(self, states=None, state_data=None, significance=0.05, maxlags=3):
        """
        Initialize the analyzer.

        Parameters:
            states (list): List of state names.
            state_data (dict): Dictionary of DataFrames for each state.
            significance (float): Significance level for the ADF test and p-value threshold.
            maxlags (int): Desired maximum number of lags for VAR lag order selection.
        """
        self.significance = significance
        self.maxlags = maxlags
        self.states = (
            states if states is not None else [f"State_{i}" for i in range(1, 51)]
        )
        self.state_data = state_data if state_data is not None else self.simulate_data()
        self.state_var_results = {}
        self.global_var_result = None
        self.relationship_matrix = None

    def simulate_data(self):
        """
        Simulate time series data for each state.

        Returns:
            dict: Dictionary mapping each state to a DataFrame of shape (12, 22).
        """
        simulated_data = {}
        np.random.seed(42)
        for state in self.states:
            # Simulate 12 time points and 22 variables of random data.
            data = np.random.randn(12, 22)
            df = pd.DataFrame(data, columns=[f"Var_{j}" for j in range(1, 23)])
            # Create a time index (monthly observations)
            df.index = pd.date_range(start="2024-01-01", periods=12, freq="M")
            simulated_data[state] = df
        return simulated_data

    @staticmethod
    def check_stationarity(series, significance=0.05):
        """
        Perform the Augmented Dickey-Fuller (ADF) test on a series.

        Parameters:
            series (pd.Series): Time series data.
            significance (float): Significance level for the test.

        Returns:
            tuple: (is_stationary (bool), p_value (float))
        """
        result = adfuller(series.dropna())
        p_value = result[1]
        return (p_value < significance), p_value

    def difference_if_needed(self, df):
        """
        Check each column for stationarity and difference the DataFrame if needed.

        Parameters:
            df (pd.DataFrame): The DataFrame to check.

        Returns:
            tuple: (possibly differenced DataFrame, flag indicating if differencing was applied)
        """
        non_stationary_found = False
        for col in df.columns:
            stationary, _ = self.check_stationarity(df[col], self.significance)
            if not stationary:
                non_stationary_found = True
                break
        if non_stationary_found:
            df_diff = df.diff().dropna()
            return df_diff, True
        else:
            return df, False

    @staticmethod
    def compute_allowed_maxlags(n_obs, n_vars):
        """
        Compute the maximum allowed lag order given the degrees-of-freedom requirements.

        For a VAR with lag order L, the number of parameters per equation is L*n_vars + 1.
        With n_obs observations (after differencing), we require:

            n_obs - L > L*n_vars + 1

        This method returns the largest integer L satisfying this (or 0 if none exists).

        Parameters:
            n_obs (int): Number of observations.
            n_vars (int): Number of variables in the VAR.

        Returns:
            int: Maximum lag order allowed.
        """
        # Try lag orders from 1 up to (n_obs - 1) and return the largest L that satisfies the inequality.
        allowed = 0
        for L in range(1, n_obs):
            if n_obs - L > L * n_vars + 1:
                allowed = L
            else:
                break
        return allowed

    def fit_state_level_models(self):
        """
        Fit VAR models for each state individually.
        For each state:
          - Check for stationarity (and difference if needed).
          - Compute an allowed maximum lag based on degrees-of-freedom.
          - If allowed lags are at least 1, select the optimal lag order using AIC.
          - Fit the VAR model and store the results.
        """
        print("Fitting state-level VAR models...\n")
        for state, df in self.state_data.items():
            print(f"Processing {state}...")
            df_stationary, differed = self.difference_if_needed(df)
            n_obs = len(df_stationary)
            n_vars = df_stationary.shape[1]

            allowed_maxlags = self.compute_allowed_maxlags(n_obs, n_vars)
            if allowed_maxlags < 1:
                print(
                    f"  [Warning] Not enough observations to estimate a VAR model for {state} "
                    f"(n_obs={n_obs}, n_vars={n_vars}, allowed_maxlags={allowed_maxlags}). Skipping.\n"
                )
                continue

            # Use the smaller of the desired maxlags and the allowed maximum.
            local_maxlags = min(self.maxlags, allowed_maxlags)
            model = VAR(df_stationary)
            try:
                lag_order_results = model.select_order(maxlags=local_maxlags)
                selected_lag = lag_order_results.aic
                if selected_lag == 0:
                    selected_lag = 1  # Force at least one lag.
                var_result = model.fit(selected_lag)
            except Exception as e: # pylint: disable=broad-exception-caught
                print(f"  [Error] VAR estimation failed for {state}: {e}\n")
                continue

            self.state_var_results[state] = {
                "lag_order": selected_lag,
                "model_summary": var_result.summary(),
                "model_params": var_result.params,
            }

            print(var_result.summary())
            print("\n" + "-" * 80 + "\n")

    def fit_global_model(self):
        """
        Combine state data and fit a global VAR model to capture inter-state relationships.
        Steps:
          - Concatenate the state DataFrames along columns.
          - Flatten the MultiIndex columns.
          - Check stationarity and difference if needed.
          - Compute an allowed maximum lag.
          - Fit the VAR model.
        """
        print("Fitting global VAR model...\n")
        # Combine data along columns. This creates a MultiIndex.
        combined_df = pd.concat(self.state_data, axis=1)
        # Flatten the MultiIndex for columns, e.g., "State_X_Var_Y".
        combined_df.columns = [f"{state}_{var}" for state, var in combined_df.columns]

        # Check stationarity for each series; if any series is non-stationary, difference the entire DataFrame.
        non_stationary_global = False
        for col in combined_df.columns:
            stationary, _ = self.check_stationarity(combined_df[col], self.significance)
            if not stationary:
                non_stationary_global = True
                break
        if non_stationary_global:
            combined_df = combined_df.diff().dropna()

        n_obs = len(combined_df)
        n_vars = combined_df.shape[1]
        allowed_maxlags = self.compute_allowed_maxlags(n_obs, n_vars)
        if allowed_maxlags < 1:
            print(
                f"  [Warning] Not enough observations to estimate a global VAR model "
                f"(n_obs={n_obs}, n_vars={n_vars}, allowed_maxlags={allowed_maxlags}). "
                f"Proceeding with lag order set to 1 (estimation may fail)."
            )
            local_maxlags = 1
        else:
            local_maxlags = min(self.maxlags, allowed_maxlags)

        global_model = VAR(combined_df)
        try:
            global_lag_results = global_model.select_order(maxlags=local_maxlags)
            global_selected_lag = global_lag_results.aic
            if global_selected_lag == 0:
                global_selected_lag = 1
            self.global_var_result = global_model.fit(global_selected_lag)
            print("Global VAR Model Summary:")
            print(self.global_var_result.summary())
            print("\n" + "=" * 80 + "\n")
        except Exception as e: # pylint: disable=broad-exception-caught
            print(f"Error fitting global VAR model: {e}")
            self.global_var_result = None

    def analyze_coefficients(self):
        """
        Analyze the coefficients of the global VAR model to identify statistically significant
        inter-state relationships.

        The analysis computes p-values from the t-statistics and aggregates counts of significant
        lagged coefficients into a relationship matrix (states as rows and columns).
        """
        if self.global_var_result is None:
            print("Global VAR model is not available. Skipping coefficient analysis.")
            return

        tvalues = self.global_var_result.tvalues
        params = self.global_var_result.params
        dof = self.global_var_result.df_resid  # Degrees of freedom

        # Compute two-tailed p-values from t-statistics.
        p_values = 2 * (1 - t_dist.cdf(np.abs(tvalues), df=dof))

        # Initialize a relationship matrix (rows: target states, columns: predictor states).
        rel_matrix = pd.DataFrame(0, index=self.states, columns=self.states)

        # The dependent variables in the global model are named like "State_X_Var_Y".
        # Coefficient names (except the intercept) are like "L1.State_X_Var_Y".
        for dep_var in params.index:
            tokens = dep_var.split("_")
            if len(tokens) < 2:
                continue  # Skip unexpected format
            dep_state = "_".join(tokens[:2])

            for coef in params.columns:
                if coef == "const":
                    continue  # Skip intercept

                try:
                    lag_info, var_name = coef.split(".", 1)
                except ValueError:
                    continue  # Skip coefficients not following the expected pattern

                tokens_coef = var_name.split("_")
                if len(tokens_coef) < 2:
                    continue
                lagged_state = "_".join(tokens_coef[:2])

                # Check significance using the p-value threshold.
                p_val = p_values.loc[dep_var, coef]
                if p_val < self.significance:
                    if (
                        lagged_state in rel_matrix.columns
                        and dep_state in rel_matrix.index
                    ):
                        rel_matrix.loc[dep_state, lagged_state] += 1

        self.relationship_matrix = rel_matrix

    def visualize_relationships(self):
        """
        Visualize the significant inter-state relationships using a heatmap and a network graph.
        The heatmap shows counts of significant lagged coefficients.
        The network graph displays directed edges from predictor state to target state.
        """
        if self.relationship_matrix is None:
            print("Relationship matrix is not available. Skipping visualization.")
            return

        # Heatmap visualization.
        plt.figure(figsize=(12, 10))
        sns.heatmap(self.relationship_matrix, annot=True, fmt="d", cmap="YlGnBu")
        plt.title(
            "Significant Inter-State Relationships\n(Count of Significant Lagged Coefficients)"
        )
        plt.xlabel("Lagged (Predictor) State")
        plt.ylabel("Dependent (Target) State")
        plt.tight_layout()
        plt.show()

        # Network graph visualization.
        G = nx.DiGraph()
        G.add_nodes_from(self.states)

        # Add directed edges: an edge from state j to state i indicates that lagged variables
        # from state j significantly predict variables in state i.
        for target_state in self.relationship_matrix.index:
            for source_state in self.relationship_matrix.columns:
                weight = self.relationship_matrix.loc[target_state, source_state]
                if weight > 0:
                    G.add_edge(source_state, target_state, weight=weight)

        plt.figure(figsize=(12, 12))
        pos = nx.spring_layout(G, seed=42)
        edges = G.edges(data=True)
        edge_weights = [d["weight"] for (_, _, d) in edges]

        nx.draw_networkx_nodes(G, pos, node_size=700, node_color="lightblue")
        nx.draw_networkx_edges(
            G, pos, width=edge_weights, arrowstyle="->", arrowsize=20
        )
        nx.draw_networkx_labels(G, pos, font_size=10)
        plt.title("Network Graph of Significant Inter-State Relationships")
        plt.axis("off")
        plt.tight_layout()
        plt.show()

    def interpret_results(self):
        """
        Print an example interpretation of the results.

        The interpretation focuses on how to read the relationship matrix to identify strong
        predictive relationships between states.
        """
        print("\nExample Interpretation:")
        print("-" * 50)
        print(
            "The relationship matrix displays counts of statistically significant lagged coefficients\n"
            "between states. For example, if the cell at row 'State_10' and column 'State_5' has a value of 3,\n"
            "this indicates that three lagged variables from State_5 are significant predictors of variables\n"
            "in State_10. Such relationships can help identify which states' time series influence others,\n"
            "potentially signaling spillover effects or shared dynamics. Further investigation of these pairs\n"
            "may reveal underlying economic, social, or other factors driving these interactions."
        )
        print("-" * 50 + "\n")

    def run_analysis(self):
        """
        Run the complete analysis: state-level VAR models, global VAR model, coefficient analysis,
        visualization, and result interpretation.
        """
        self.fit_state_level_models()
        self.fit_global_model()
        self.analyze_coefficients()
        self.visualize_relationships()
        self.interpret_results()


if __name__ == "__main__":
    analyzer = VARModelAnalyzer(maxlags=3)
    analyzer.run_analysis()
