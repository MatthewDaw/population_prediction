from projen.python import PythonProject

AUTHORS = ["Matthew Daw"]
AUTHOR_EMAIL = "mattdaw7@gmail.com"
AWS_PROFILE_NAME = "sandbox"

ROOT_PROJECT = PythonProject(
    author_email="md@getChief.com",
    author_name="MatthewDaw",
    module_name="population_data_analysis",
    name="population-data-analysis",
    version="0.1.0",
    poetry=True,
    pytest=False,
    deps=["pre-commit", "python-dotenv@^0.21.0", "python@^3.12.0"],
    dev_deps=[
        "pre-commit",
    ],
)

ROOT_PROJECT.add_git_ignore(".env")
ROOT_PROJECT.add_git_ignore(".env.secrets")

DBT_NAME = "population_analysis_dbt"
DBT_PROJECT = PythonProject(
    parent=ROOT_PROJECT,
    author_email=AUTHOR_EMAIL,
    author_name=AUTHORS[0],
    module_name=DBT_NAME.replace("-", "_"),
    name=DBT_NAME,
    outdir=DBT_NAME,
    version="0.0.0",
    description="Module only for API contracts between services.",
    poetry=True,
    deps=[
        "python@^3.12.0",
        "structlog@^24.2.0",
        "pydantic-settings@^2.2.1",
        "python-dotenv@^0.21.0",
        "pandas",
    ],
)

EXPERIMENTS_NAME = "experiments"
EXPERIMENTS_PROJECT = PythonProject(
    parent=ROOT_PROJECT,
    author_email=AUTHOR_EMAIL,
    author_name=AUTHORS[0],
    module_name=EXPERIMENTS_NAME.replace("-", "_"),
    name=EXPERIMENTS_NAME,
    outdir=EXPERIMENTS_NAME,
    version="0.0.0",
    description="Module only for API contracts between services.",
    poetry=True,
    deps=[
        "python@^3.12.0",
        "structlog@^24.2.0",
        "pydantic-settings@^2.2.1",
        "python-dotenv@^0.21.0",
        "pandas",
        "matplotlib",
        "statsmodels",
        "mlflow",
        "seaborn",
        "snowflake-connector-python",
        "cachetools",
    ],
)

POPULATION_DATA_ANALYSIS_NAME = "population_data_analysis"
POPULATION_DATA_ANALYSIS_PROJECT = PythonProject(
    parent=ROOT_PROJECT,
    author_email=AUTHOR_EMAIL,
    author_name=AUTHORS[0],
    module_name=POPULATION_DATA_ANALYSIS_NAME.replace("-", "_"),
    name=POPULATION_DATA_ANALYSIS_NAME,
    outdir=POPULATION_DATA_ANALYSIS_NAME,
    version="0.0.0",
    description="Module only for API contracts between services.",
    poetry=True,
    deps=[
        "python@^3.12.0",
        "structlog@^24.2.0",
        "pydantic-settings@^2.2.1",
        "python-dotenv@^0.21.0",
        "pandas",
        "matplotlib",
        "statsmodels",
        "mlflow",
        "seaborn",
        "snowflake-connector-python",
        "cachetools",
    ],
)

ROOT_PROJECT.synth()
DBT_PROJECT.synth()
EXPERIMENTS_PROJECT.synth()
POPULATION_DATA_ANALYSIS_PROJECT.synth()
