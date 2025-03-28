# oic_model_server/services/predict_service.py
import pandas as pd

import pickle

import numpy as np

from typing import List

from sqlmodel import Session, select

from oic_model_server.models.predict import HousePredictionRequest, PredictTable


class PredictionService:
    """
    Servicio para realizar predicciones de precio de casas.

    Este servicio carga el pipeline entrenado desde un archivo `pickle` y lo utiliza para predecir el logaritmo del precio de la propiedad.
    Además, registra la predicción en la base de datos.
    
    :param model_path: Ruta al archivo `pickle` que contiene el pipeline entrenado.
    :type model_path: str
    :param db: Sesión de `SQLModel` para interactuar con la base de datos.
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
        Realiza la predicción del precio del predio a partir de las características proporcionadas.
        
        \f        

        :param data: Datos de entrada para la predicción.
        :type data: HousePredictionRequest
        :return: Valor predicho como número flotante.
        :rtype: float

        :raises Exception: Si ocurre un error durante la predicción o al registrar la predicción en la base de datos.
        """
        features = data.model_dump()
        df_input = pd.DataFrame([features])
        
        try:
            
            log_prediction = self.model.predict(df_input)
            predicted = float(np.exp(float(log_prediction[0])))
          
        except Exception as e:
            raise Exception(f"Error durante la predicción: {e}")
        
        try:
            
            record = PredictTable(
                user_name=data.user_name,
                feature_data=data.model_dump(),
                prediction=predicted
            )
            self.db.add(record)
            self.db.commit()
            self.db.refresh(record)
            
        except Exception as e:
            self.db.rollback()
            raise Exception(f"Error al guardar la predicción en la base de datos: {e}")
        
        return predicted
    
    
    def get_predictions_by_user(self, user_name: str) -> List[PredictTable]:
        """
        Obtiene todas las predicciones realizadas por un usuario específico.
        
        Este método consulta la base de datos para recuperar todas las predicciones
        asociadas con el nombre de usuario proporcionado, ordenadas por fecha de creación
        de la más reciente a la más antigua.
        
        \f
        
        :param user_name: Nombre del usuario cuyas predicciones se desean obtener
            
        :return List[PredictTable]: Lista de registros de predicciones del usuario
        """
        try:
            query = select(PredictTable).where(
                PredictTable.user_name == user_name
            ).order_by(PredictTable.created_at.desc())
            
            results = self.db.exec(query).all()
            return results
            
        except Exception as e:
            raise Exception(f"Error al obtener las predicciones del usuario: {e}")
