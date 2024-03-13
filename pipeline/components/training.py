from kfp import dsl
from kfp.dsl import Dataset, Output, Input, Metrics, Model


@dsl.component(
    base_image="python:3.9",
    packages_to_install=["pandas>=2.2", "scikit-learn>=1.0", "pandas-gbq"],
)
def train_model(
    dataset_input: Input[Dataset],
    model_output: Output[Model],
    metrics_training: Output[Metrics],
):
    """
    Loads a CSV File and trains a model
    """

    from sklearn import svm
    import pandas as pd
    import joblib

    df = pd.read_csv(dataset_input.path)

    train_df = df[df["split"] == "train"]
    test_df = df[df["split"] == "test"]

    x_train = train_df[df.columns[:-2]].values
    y_train = train_df["target"].values

    x_test = test_df[df.columns[:-2]].values
    y_test = test_df["target"].values

    # Train a SVM model
    model = svm.SVC()
    model.fit(x_train, y_train)

    # Evaluate the model on train
    acc_train = model.score(x_train, y_train)
    print(f"Accuracy Train: {acc_train}")
    metrics_training.log_metric("acc_train", acc_train)

    # Evaluate the model on test
    acc_test = model.score(x_test, y_test)
    print(f"Accuracy Test: {acc_test}")
    metrics_training.log_metric("acc_test", acc_test)

    # Save the model
    joblib.dump(model, model_output.path)

    # Store predictions on Bigquery
    test_df["prediction"] = model.predict(x_test)
    test_df["timestamp"] = pd.Timestamp.now()
    # remove target and split columns
    test_df = test_df.drop(columns=["target", "split"])

    test_df.to_gbq("sapiens-417017.predictions.training", project_id="sapiens-417017",if_exists="append")