from sklearn.datasets import load_iris
from sklearn import svm
import pandas as pd


# Load the iris dataset
iris = load_iris()

# to pandas
iris_df = pd.DataFrame(data=iris.data, columns=iris.feature_names)
iris_df["target"] = iris.target

# Split ( add a column with the split)
iris_df["split"] = "train"
iris_df.loc[iris_df.sample(frac=0.2, random_state=42).index, "split"] = "test"

print(iris_df)

# Train a SVM model
model = svm.SVC()
train_df = iris_df[iris_df["split"] == "train"]
x_train = train_df[iris.feature_names]
y_test = train_df["target"]

model.fit(x_train, y_test)

# Evaluate the model on test
test_df = iris_df[iris_df["split"] == "test"]

x_test = test_df[iris.feature_names]
y_test = test_df["target"]

y_test_pred = model.predict(x_test)

# Print the accuracy
print(f"Accuracy: {sum(y_test_pred == y_test) / len(y_test)}")

# Store model 
import joblib
joblib.dump(model, "model.joblib")
