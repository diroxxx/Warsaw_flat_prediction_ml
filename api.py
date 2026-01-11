"""
API for real estate price prediction using FastAPI.
"""

from pathlib import Path
import uvicorn
from fastapi import FastAPI, HTTPException
from starlette import status

from model.input_model import PredictionInput, District, ConstructionStatus, Market
from model.model_function import predict

BASE_DIR = Path(__file__).resolve(strict=True).parent
MODEL_DIR = BASE_DIR.joinpath("ml_model")
DATA_DIR = BASE_DIR.joinpath("data")

app = FastAPI()

@app.get("/model/options", tags=["model"], status_code=status.HTTP_200_OK)
async def get_options():
    """Endpoint to get available options for categorical features."""
    return {
        "districts": [d.value for d in District],
        "construction_statuses": [s.value for s in ConstructionStatus],
        "markets": [m.value for m in Market],
    }

@app.post("/model/predict", tags=["model"], status_code=status.HTTP_200_OK)
async def predict_price(input_data: PredictionInput, model_name: str = "flat_model"):
    """Endpoint to predict the price using the trained model."""
    model_file = MODEL_DIR.joinpath(f"{model_name}.pkl")

    if not (10 < input_data.surface < 500):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="`surface` must be > 10 and < 500"
        )


    if not model_file.exists():
        raise HTTPException(status_code=400, detail="Model not found.")

    prediction = predict(model_file, input_data)
    formatted = f"{prediction:.2f}"
    return {"predicted_price": formatted}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8008)