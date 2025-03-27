# oic_model_server/api/routes/predict.py
from fastapi import APIRouter, Depends, HTTPException

from typing import List

from sqlmodel import Session, select

from oic_model_server.core.database import get_db

from oic_model_server.models.predict import HousePredictionRequest, PredictionResponse, PredictTable

from oic_model_server.services.predict_service import PredictionService


router = APIRouter()


MODEL_PATH = "artifacts/modelo_lineal_v0.1.0.pkl"


@router.post("/predict", response_model=dict)
def predict_house_price(request: HousePredictionRequest, db: Session = Depends(get_db)):
    """
    Endpoint para predecir el precio de una casa y registrar la predicción en la base de datos.
    """
    service = PredictionService(model_path=MODEL_PATH, db=db)
    try:
        predicted_price = service.predict(request)
        return {"predicted_price": predicted_price}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    
@router.get("/predictions/{user_name}", response_model=List[PredictionResponse])
def get_user_predictions(user_name: str, db: Session = Depends(get_db)):
    """
    Obtiene todas las predicciones realizadas por un usuario específico.
    \f    
    
    :param user_name: Nombre del usuario cuyas predicciones se quieren consultar
    :type user_name: str
    :param db: Sesión de base de datos (inyectada por FastAPI)
    :type db: Session
    :return: Lista de registros de predicciones del usuario
    :rtype: List[PredictionResponse]
    :raises HTTPException: Si no se encuentran predicciones para el usuario o si ocurre otro error
    """
    service = PredictionService(model_path=MODEL_PATH, db=db)
    try:
        predictions = service.get_predictions_by_user(user_name)
        
        if not predictions:
            raise HTTPException(
                status_code=404, 
                detail=f"No se encontraron predicciones para el usuario: {user_name}"
            )
            
        return predictions
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener predicciones: {str(e)}")
