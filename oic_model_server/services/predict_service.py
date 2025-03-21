# oic_model_server/services/predict_service.py
import random

from sqlmodel import Session

from oic_model_server.models.predict import PredictTable, PredictRequest


class PredictService:
    """
    Servicio de predicción.

    Proporciona la lógica para predecir el valor de venta de una propiedad a partir de sus características.
    Esta implementación guarda la predicción en la base de datos.
    """

    def __init__(self, db: Session):
        """
        Inicializa el servicio con una sesión de base de datos.

        :param db: Sesión activa para interactuar con la base de datos.
        :type db: Session
        """
        self.db = db

    def predict(self, request: PredictRequest, user_name: str) -> PredictTable:
        """
        Realiza una predicción simulada y la guarda en la base de datos.

        :param request: Datos de entrada con las características del inmueble.
        :type request: PredictRequest
        :param user_name: Nombre del usuario que solicita la predicción.
        :type user_name: str
        :return: Valor de venta predicho (simulado).
        :rtype: float
        """
        prediction_value = round(random.uniform(200000, 500000), 2)

        prediction_record = PredictTable(
            user_name=user_name,
            feature_data=request.dict(),
            prediction=prediction_value
        )

        self.db.add(prediction_record)
        self.db.commit()
        self.db.refresh(prediction_record)

        return prediction_record
