from fastapi import FastAPI
import tools
import joblib

# Load the model
model = tools.load_model()

# Create an instance of the FastAPI class
app = FastAPI()


# Define a route for the root endpoint
@app.get("/")
async def read_root():
    return {"message": "Welcome to the IRIS Model Server"}


# Define a route for the /predict endpoint
@app.post("/predict")
async def predict(sepal_l: float, sepal_w: float, petal_l: float, petal_w: float):
    """
    Make a prediction based on the input data
    """

    prediction = model.predict([[sepal_l, sepal_w, petal_l, petal_w]])
    prediction = int(prediction[0])

    return {"species": prediction}
