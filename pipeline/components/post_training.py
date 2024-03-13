from kfp import dsl
from kfp.dsl import Model, Dataset, Output, Input, Metrics


@dsl.component(
    base_image="python:3.9",
    packages_to_install=[
        "pandas>=2.2",
        "scikit-learn>=1.0",
        "google-cloud-secret-manager",
    ],
)
def register_model(
    model_input: Input[Model],
):
    """
    Register the model uri into a gcp secret
    """
    import os
    from google.cloud import secretmanager

    # Get the model uri
    model_uri = model_input.uri

    # Get the project id
    project_id = "sapiens-417017"

    # Create the secret manager client
    client = secretmanager.SecretManagerServiceClient()

    # Create the secret name
    secret_name = f"projects/{project_id}/secrets/iris_model"

    # Add the secret
    response = client.add_secret_version(
        request={"parent": secret_name, "payload": {"data": model_uri.encode("utf-8")}}
    )

    print(f"Added model to secret 'iris_model'")
