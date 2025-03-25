# oic_model_server/api/routes/predict.py
from fastapi import APIRouter, Depends, HTTPException

from sqlmodel import Session, select

from oic_model_server.core.database import get_db

from oic_model_server.models.user import UserTable

from oic_model_server.models.predict import PredictRequest, PredictResponse

from oic_model_server.services.predict_service import PredictService


router = APIRouter()


@router.post("/", response_model=PredictResponse)
def predecir(request: PredictRequest, user_name: str, db: Session = Depends(get_db)):
    """
    Endpoint para realizar una predicción de valor de venta y registrar el resultado en la base de datos.
    \f

    :param request: Datos de entrada del inmueble (área, habitaciones, ubicación).
    :type request: PredictRequest
    :param user_name: Nombre del usuario que solicita la predicción.
    :type user_name: str
    :param db: Sesión de base de datos inyectada por FastAPI.
    :type db: Session
    :return: Valor de venta predicho.
    :rtype: PredictResponse
    """
    user = db.exec(select(UserTable).where(UserTable.user_name == user_name)).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado.")

    service = PredictService(db)
    prediction_record = service.predict(request=request, user_name=user_name)

    return PredictResponse.model_validate({"prediction": prediction_record.prediction})
