from kfp import dsl
from kfp.dsl import Dataset, Output, Input


@dsl.component(base_image="python:3.9", packages_to_install=["pandas>=2.2"])
def clean_dataset(dataset: str, dataset_output: Output[Dataset]):
    """
    Loads a CSV File and returns
    """

    import pandas as pd

    df = pd.read_csv(dataset)

    # Drop missing values
    df = df.dropna()

    # Rename columns to match the BigQuery schema
    df = df.rename(
        {
            "sepal length (cm)": "sepal_l",
            "sepal width (cm)": "sepal_w",
            "petal length (cm)": "petal_l",
            "petal width (cm)": "petal_w",
        },
        axis="columns",
    )

    # Save the cleaned dataset
    df.to_csv(dataset_output.path, index=False)


@dsl.component(base_image="python:3.9", packages_to_install=["pandas>=2.2"])
def split_dataset(dataset_input: Input[Dataset], dataset_output: Output[Dataset]):
    """
    Loads a CSV File and adds a column with the split
    """

    import pandas as pd

    df = pd.read_csv(dataset_input.path)

    # Split the dataset
    df["split"] = "train"
    df.loc[df.sample(frac=0.2, random_state=42).index, "split"] = "test"

    # Save the splitted dataset
    df.to_csv(dataset_output.path, index=False)
