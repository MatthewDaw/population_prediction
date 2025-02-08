from projen.python import PythonProject

project = PythonProject(
    author_email="md@getchief.com",
    author_name="Matthew Daw",
    module_name="population_data_analysis",
    name="population_data_analysis",
    version="0.1.0",
)

project.synth()