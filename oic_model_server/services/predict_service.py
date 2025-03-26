# oic_model_server/services/predict_service.py
import pandas as pd

import pickle

from sqlmodel import Session

from oic_model_server.models.predict import HousePredictionRequest, PredictTable


class PredictionService:
    """
    Servicio para realizar predicciones de precio de casas.

    Este servicio carga un pipeline entrenado (incluyendo el preprocesamiento y el modelo)
    desde un archivo pickle y lo utiliza para predecir el precio (en logaritmo) a partir
    de las características proporcionadas en una solicitud. Además, guarda el registro de
    la predicción en la base de datos.

    :param model_path: Ruta al archivo pickle que contiene el pipeline entrenado.
    :type model_path: str
    :param db: Sesión de SQLModel para interactuar con la base de datos.
    :type db: Session
    """
    def __init__(self, model_path: str, db: Session):
        self.db = db
        try:
            with open(model_path, "rb") as f:
                self.model = pickle.load(f)
        except Exception as e:
            raise Exception(f"Error al cargar el modelo: {e}")

    def predict(self, data: HousePredictionRequest) -> float:
        """
        Realiza la predicción del precio (log_price) de una casa a partir de las características
        proporcionadas y registra el resultado en la base de datos.

        :param data: Solicitud con las características de la casa para la predicción.
        :type data: HousePredictionRequest
        :return: Valor predicho (log_price) como número de punto flotante.
        :rtype: float

        :raises Exception: Si ocurre un error durante la predicción o al guardar el registro en la base de datos.
        """        
        features = data.model_dump()
        df_input = pd.DataFrame([features])
        
        try:
            prediction = self.model.predict(df_input)
            predicted_value = float(prediction[0])
        except Exception as e:
            raise Exception(f"Error durante la predicción: {e}")
        
        try:
            record = PredictTable(
                user_name=data.user_name,
                feature_data=data.model_dump(),
                prediction=predicted_value
            )
            self.db.add(record)
            self.db.commit()
            self.db.refresh(record)
        except Exception as e:
            self.db.rollback()
            raise Exception(f"Error al guardar la predicción en la base de datos: {e}")

        return predicted_value
