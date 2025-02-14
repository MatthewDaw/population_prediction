import matplotlib.pyplot as plt
import pandas as pd


class Visualizer:

    def plot_true_and_predictions(self, true_df: pd.DataFrame, pred_df: pd.DataFrame):
        """
        Plots the full true DataFrame and overlays the predicted values for the last rows.

        Parameters:
            true_df (pd.DataFrame): DataFrame containing the full set of true values. The index
                                    should represent time or sequential ordering.
            pred_df (pd.DataFrame): DataFrame containing predicted values for the last few rows of
                                    true_df. It must have the same column names as true_df.

        Notes:
            - If pred_df's index does not match the corresponding tail of true_df, then this
              function reassigns the last len(pred_df) indices from true_df to pred_df.
        """
        # Determine number of prediction rows.

        n_pred = pred_df.shape[0]

        # Assign the last n_pred indices from true_df to pred_df.
        pred_df = pred_df.copy()  # avoid modifying the original DataFrame
        pred_df.index = true_df.index[-n_pred:]

        plt.figure(figsize=(12, 6))

        # Plot the full true series for each column.
        for col in true_df.columns:
            plt.plot(true_df.index, true_df[col], label=f"{col} True", marker="o")

        # Overlay the predictions with a different style.
        for col in pred_df.columns:
            plt.plot(
                true_df.index[-1 * len(pred_df) :],
                pred_df[col],
                label=f"{col} Predicted",
                linestyle="--",
                marker="x",
                markersize=10,
            )

        plt.xlabel("Time")
        plt.ylabel("Value")
        plt.title("True Values and Predictions")
        plt.legend()
        plt.grid(True)
        plt.show()
