"""
    Creates a bucket with a dataset example CSV File
"""

from pulumi_gcp import storage
from sklearn.datasets import load_iris
import pandas as pd

# Create a GCP resource (Storage Bucket)
bucket = storage.Bucket("sapiens_dataset", name="sapiens_dataset", location="US")

# Create a CSV Example File
iris_dataset = load_iris()
iris_df = pd.DataFrame(data=iris_dataset.data, columns=iris_dataset.feature_names)
iris_df["target"] = iris_dataset.target
iris_df.to_csv("iris.csv", index=False)

# Create a GCP resource (Storage Bucket Object)
object = storage.BucketObject(
    "iris_csv", name="iris.csv", bucket=bucket.name, source="iris.csv"
)
