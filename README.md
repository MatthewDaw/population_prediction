# Population Data Analysis Project

## Overview

This project is designed to perform data analysis and machine learning operations on population data. It includes various components such as data loaders, machine learning models, and experiment suites.

## Registering New Experiments

To register new experiments, you need to modify the experiment suites and SDKs. Below are the steps to guide you through the process:

### 1. Adding to Experiment Suites

Experiment suites are defined in the `models_experiments_suite.py` file. To add a new experiment:

- **Define a new `ParameterDecisionSuite`:** This involves specifying the function name, parameter suite name, associated Pydantic model, and parameter choices.
- **Example:**

  ```python
  from population_data_analysis.sweep_generation_tools.config_list_generation import ParameterDecisionSuite, ParameterChoice
  from population_data_analysis.sweep_generation_tools import SweepConfig

  new_model_parameter_suite = ParameterDecisionSuite(
      function_name=AvailableMLOperations.new_operation,
      parameter_suite_name="new_operation_suite",
      associated_pydantic_model=NewOperationHyperparameters,
      parameter_choices=[
          ParameterChoice(
              parameter_name="new_param",
              parameter_value=SweepConfig(type='int', min=1, max=10, samples=5, default=5)
          ),
      ]
  )
  model_parameter_suites.append(new_model_parameter_suite)
  ```

### 2. Extending SDKs

SDKs are responsible for executing operations. To extend an SDK:

- **Modify the `run` method:** Add a new condition for your operation and implement the logic to handle it.
- **Example:**

  ```python
  class MLModelsSDK:
      """SDK for ML models operations."""

      def run(self, train_data: pd.DataFrame, steps: int, operation: AvailableMLOperations, hyperparameters: Union[VARHyperparameters, VARMAXHyperparameters, NewOperationHyperparameters]) -> np.ndarray:
          """Run an operation."""
          if operation == AvailableMLOperations.new_operation:
              model = NewOperationModelContainer(hyperparameters)
          # existing conditions...
          else:
              raise ValueError("Operation not found.")
          forecasted_values = model.fit_forecast(train_data, steps=steps)
          return forecasted_values
  ```

### 3. Implementing New Models

If your new experiment requires a new model:

- **Create a new model container:** Implement the logic for fitting and forecasting within this container.
- **Example:**

  ```python
  class NewOperationModelContainer:
      def __init__(self, hyperparameters):
          # Initialize model with hyperparameters

      def fit_forecast(self, train_data, steps):
          # Implement fitting and forecasting logic
          return forecasted_values
  ```

## Conclusion

By following these steps, you can extend the functionality of the population data analysis project to include new experiments and operations. Ensure that all new components are thoroughly tested and documented.

This guide provides a structured approach to adding new experiments and operations to your project, ensuring that users can easily extend its capabilities.