"""Orchestrates all experiments."""

import mlflow
from mlflow.tracking import MlflowClient

from population_data_analysis.generate_all_experiment_run_configs import (
    ModelParameterIterator,
)
from population_data_analysis.pipeline_operations.experiments_pipeline_sdk import (
    ExperimentsSDK,
)

mlflow.set_tracking_uri(uri="http://127.0.0.1:8080")


class RootExperimentOrchestrator:
    """Orchestrates all experiments."""

    def __init__(self):
        self.model_seep_generator = ModelParameterIterator()
        self.experiment_sdk = ExperimentsSDK()
        self.ml_flow_client = MlflowClient()

    def restore_experiment(self, experiment_name):
        """Restore the experiment."""
        experiment = self.ml_flow_client.get_experiment_by_name(experiment_name)

        if experiment is not None:
            experiment_id = experiment.experiment_id
            try:
                self.ml_flow_client.restore_experiment(experiment_id)
            except Exception:  # pylint: disable=broad-except
                pass

    def run_full_sweep(self, upsert_all_previous_runs=False):
        """Run all experiments."""
        all_experiment_configs = self.model_seep_generator.generate_basic_var_sweep()

        self.restore_experiment(all_experiment_configs.experiment_name)

        mlflow.set_experiment(all_experiment_configs.experiment_name)

        for experiment_config in all_experiment_configs.experiment_run_configs:

            run_name = (
                all_experiment_configs.experiment_name
                + experiment_config.dump_to_name()
            )

            filter_string = f"tags.mlflow.runName = '{run_name}'"
            runs = mlflow.search_runs(filter_string=filter_string)

            if runs.empty or upsert_all_previous_runs:
                if not runs.empty:
                    for run_id in runs.run_id:
                        self.ml_flow_client.delete_run(run_id)
                with mlflow.start_run(run_name=run_name):
                    mlflow.set_tag("mlflow.runName", run_name)
                    self.experiment_sdk.run_experiment(experiment_config)


if __name__ == "__main__":
    orchestrator = RootExperimentOrchestrator()
    orchestrator.run_full_sweep(upsert_all_previous_runs=True)
