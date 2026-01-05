from pathlib import Path

import uvicorn
from fastapi import FastAPI, HTTPException
from starlette import status

from model.TrainInput import TrainInput
from model.PredictionInput import PredictionInput
from model.model_function import train, predict

BASE_DIR = Path(__file__).resolve(strict=True).parent
MODEL_DIR = BASE_DIR.joinpath("ml_model")
DATA_DIR = BASE_DIR.joinpath("data")

app = FastAPI()

@app.post("/model/train", tags=["model"], status_code=status.HTTP_201_CREATED)
async def train_model(
    train_data: TrainInput,
    data_train_name: str = "warsaw_flat",
    model_name: str = "rfm_model",
):
    """Endpoint to train the model with new data."""
    data_file = DATA_DIR.joinpath(f"{data_train_name}.csv")
    model_file = MODEL_DIR.joinpath(f"{model_name}.pkl")

    if not model_file.exists():
        raise HTTPException(status_code=400, detail="Model not found.")

    if not data_file.exists():
        raise HTTPException(status_code=400, detail="Training data not found.")

    train(train_data, data_file, model_file)
    return {"message": "Model trained successfully"}


@app.post("/model/predict", tags=["model"], status_code=status.HTTP_200_OK)
async def predict_price(input_data: PredictionInput, model_name: str = "rfm_model"):
    """Endpoint to predict the price using the trained model."""
    model_file = MODEL_DIR.joinpath(f"{model_name}.pkl")

    if not model_file.exists():
        raise HTTPException(status_code=400, detail="Model not found.")

    prediction = predict(model_file, input_data)
    return {"predicted_price": prediction}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8008)