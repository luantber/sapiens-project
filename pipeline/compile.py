from kfp import dsl
from kfp import compiler

from components.data_preprocessing import clean_dataset, split_dataset
from components.training import train_model
from components.post_training import register_model


@dsl.pipeline
def training_pipeline(dataset_uri: str):
    clean_dataset_op = clean_dataset(dataset=dataset_uri).set_cpu_limit("1")
    split_dataset_op = split_dataset(
        dataset_input=clean_dataset_op.outputs["dataset_output"]
    ).set_cpu_limit("1")

    # Train the model
    training_op = train_model(
        dataset_input=split_dataset_op.outputs["dataset_output"]
    ).set_cpu_limit("1")

    # Register the model
    register_model_op = register_model(
        model_input=training_op.outputs["model_output"]
    ).set_cpu_limit("1")


compiler.Compiler().compile(training_pipeline, package_path="pipeline/pipeline.yaml")
