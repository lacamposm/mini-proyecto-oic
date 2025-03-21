# oic_model_server/models/prediction.py
from sqlmodel import SQLModel, Field as SQLModelField

from sqlalchemy import Column, JSON

from enum import Enum

from pydantic import BaseModel, Field

from typing import Optional, Dict



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


class PredictRequest(BaseModel):
    """
    Modelo de solicitud para realizar una predicción de valor de venta.

    Este modelo representa las características que el modelo de regresión necesita
    para estimar el valor de una propiedad.

    :param metros_cuadrados: Área construida en metros cuadrados. Debe ser mayor que 0.
    :type metros_cuadrados: float
    :param num_habitaciones: Número de habitaciones. Debe ser 0 o más.
    :type num_habitaciones: float
    :param ubicacion: Ubicación de la propiedad, debe ser una de las opciones válidas definidas en :class:`UbicacionEnum`.
    :type ubicacion: UbicacionEnum
    """
    metros_cuadrados: float = Field(..., gt=0, description="Área en metros cuadrados")
    num_habitaciones: float = Field(..., ge=0, description="Número de habitaciones")
    ubicacion: UbicacionEnum = Field(..., description="Zona de la cuidad")


class PredictResponse(BaseModel):
    """
    Modelo de respuesta que representa el valor predicho por el modelo.

    :param prediction: Valor estimado de venta para la propiedad ingresada.
    :type prediction: float
    """
    prediction: float = Field(..., description="Valor de venta predicho")
