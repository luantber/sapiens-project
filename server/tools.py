import re
from google.cloud import secretmanager
from google.cloud import storage
import joblib
from io import BytesIO

def fetch_secret(project_id, secret_id) -> str:
    """
    Fetch a secret from Secret Manager and return the value
    """
    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/{project_id}/secrets/{secret_id}/versions/latest"
    response = client.access_secret_version(request={"name": name})
    return response.payload.data.decode("UTF-8")


def parse_uri(uri: str) -> tuple[str, str]:
    """
    Parse a GCS URI into its bucket and path
    uses regex
    """
    match = re.match(r"gs://([^/]+)/(?P<path>.+)", uri)
    return match.group(1), match.group("path")


def download_model(bucket_name: str, model_path: str) -> bytes:
    """
    Download a model from GCS and return the binary data
    """
    client = storage.Client()
    bucket = client.get_bucket(bucket_name)
    blob = bucket.blob(model_path)
    model_data = blob.download_as_string()
    return model_data


def load_model():
    """
    Initialize the model
    """
    # Fetch the secret
    project_id = "sapiens-417017"
    secret_id = "iris_model"

    secret = fetch_secret(project_id, secret_id)
    # Parse the GCS URI
    bucket_name, model_path = parse_uri(secret)
    # Download the model
    model_data = download_model(bucket_name, model_path)
    # Load the model
    model = joblib.load(BytesIO(model_data))
    return model
