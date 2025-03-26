# oic_model_server/api/routes/predict.py
from fastapi import APIRouter, Depends, HTTPException

from sqlmodel import Session

from oic_model_server.core.database import get_db

from oic_model_server.models.predict import HousePredictionRequest

from oic_model_server.services.predict_service import PredictionService

router = APIRouter()


MODEL_PATH = "artifacts/modelo_lineal_v0.1.0.pkl"

@router.post("/predict", response_model=dict)
def predict_house(request: HousePredictionRequest, db: Session = Depends(get_db)):
    """
    Endpoint para predecir el precio de una casa y registrar la predicción en la base de datos.
    """
    service = PredictionService(model_path=MODEL_PATH, db=db)
    try:
        predicted_price = service.predict(request)
        return {"predicted_price": predicted_price}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
