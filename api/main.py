
from monitoring.monitor import log_prediction
from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import joblib
from pathlib import Path


# Create FastAPI application
app = FastAPI(
    title="Agricultural Crop Yield Prediction API",
    description="API for predicting crop yield using agricultural and environmental data.",
    version="1.0.0"
)


# Locate the trained model
BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = BASE_DIR / "models" / "crop_yield_model_mlflow.pkl"

# Load the trained model
model = joblib.load(MODEL_PATH)


# Input data structure
class CropYieldInput(BaseModel):
    area: str
    year: int
    average_rain_fall_mm_per_year: float
    pesticides_tonnes: float
    avg_temp: float
    item: str


# Root endpoint
@app.get("/")
def home():
    return {
        "message": "Agricultural Crop Yield Prediction API is running"
    }


# Prediction endpoint
@app.post("/predict")
def predict(data: CropYieldInput):

    # Convert input into DataFrame
    input_data = pd.DataFrame([{
        "area": data.area,
        "year": data.year,
        "average_rain_fall_mm_per_year": data.average_rain_fall_mm_per_year,
        "pesticides_tonnes": data.pesticides_tonnes,
        "avg_temp": data.avg_temp,
        "item": data.item
    }])

    # Make prediction
    prediction = model.predict(input_data)[0]
    log_prediction(data.model_dump(), prediction)
    return {
        "predicted_yield_hg_ha": round(float(prediction), 2)
    }
