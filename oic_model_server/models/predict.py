# oic_model_server/models/prediction.py
from sqlmodel import SQLModel, Field as SQLModelField

from sqlalchemy import Column, JSON

from enum import Enum

from pydantic import BaseModel, Field

from typing import Optional, Dict, Union



class PredictTable(SQLModel, table=True):
    """
    Representa un registro de predicción en la base de datos.

    Esta clase define la estructura para almacenar los datos de una predicción,
    incluyendo la información de las características en formato JSON, el valor predicho y el usuario
    asociado (mediante su nombre de usuario).

    :param id_predict: Identificador único de la predicción.
    :type id_predict: Optional[int]
    :param user_name: Nombre de usuario asociado a la predicción. Es una llave foránea que hace referencia
                      a ``users.user_name``.
    :type user_name: str
    :param feature_data: Datos de las características en formato JSON. Aquí se guarda toda la información
                         que ingresa el usuario.
    :type feature_data: Dict
    :param prediction: Valor predicho.
    :type prediction: float
    """
    __tablename__ = "predictions"

    predict_id: Optional[int] = SQLModelField(default=None, primary_key=True)
    user_name: str = SQLModelField(foreign_key="users.user_name")
    feature_data: Dict = SQLModelField(..., sa_column=Column(JSON))
    prediction: float = SQLModelField(...)


class UbicacionEnum(str, Enum):
    """
    Enumeración de ubicaciones válidas para una predicción.

    Las ubicaciones posibles son:

    - ``Centro``
    - ``Norte``
    - ``Sur``
    - ``Este``
    - ``Oeste``
    """
    centro = "Centro"
    norte = "Norte"
    sur = "Sur"
    este = "Este"
    oeste = "Oeste"


class HousePredictionRequest(BaseModel):
    user_name: str
    bedrooms: Optional[int] = None
    bathrooms: Optional[float] = None
    sqft_living: Optional[int] = None
    sqft_lot: Optional[int] = None
    floors: Optional[float] = None
    waterfront: Optional[str] = None   # ahora como cadena
    view: Optional[str] = None         # ahora como cadena
    condition: Optional[int] = None
    grade: Optional[int] = None
    sqft_above: Optional[int] = None
    sqft_basement: Optional[int] = None
    zipcode: Optional[str] = None      # ahora como cadena
    lat: Optional[float] = None
    long: Optional[float] = None
    renovated: Optional[int] = None
    lat_squared: Optional[float] = None
