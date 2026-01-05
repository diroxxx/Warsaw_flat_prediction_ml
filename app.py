

from fastapi import FastAPI, HTTPException
import uvicorn
from typing import Annotated
from pathlib import Path

from model.PredictionInput import PredictionInput
from model.modelFunction import train, predict
from starlette import status
from model.TrainInput import TrainInput

BASE_DIR = Path(__file__).resolve(strict=True).parent
MODEL_DIR = Path(BASE_DIR).joinpath("ml_model")
DATA_DIR = Path(BASE_DIR).joinpath("data")

app = FastAPI()

@app.get("/", tags=["intro"])
def read_root():
    return {"Hello": "World"}


@app.post("/model/train", tags=["model"], status_code=status.HTTP_201_CREATED)
async def train_model(train_data: TrainInput, data_train_name= "warsaw_flat", model_name="rfm_model"):

    data_file = Path(DATA_DIR).joinpath(f"{data_train_name}.csv")
    model_file = Path(MODEL_DIR).joinpath(f"{model_name}.pkl")

    if not model_file.exists():
        raise HTTPException(status_code=400, detail="Model not found.")

    if not data_file.exists():
        raise HTTPException(status_code=400, detail="Training data not found.")

    train(train_data, data_file, model_file)
    return {"message": "Model trained successfully"}

@app.post("/model/predict", tags=["model"], status_code=status.HTTP_200_OK)
async def predict_price(input_data: PredictionInput, model_name="rfm_model"):

    model_file = Path(MODEL_DIR).joinpath(f"{model_name}.pkl")

    if not model_file.exists():
        raise HTTPException(status_code=400, detail="Model not found.")

    prediction = predict(model_file, input_data)

    return {"predicted_price": prediction}


# def is_input_valid(input_data: PredictionInput) -> bool:
#     data = input_data.to_dict()



if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8008)