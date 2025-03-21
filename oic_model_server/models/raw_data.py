# oic_model_server/models/raw_data.py
from typing import Optional

from sqlmodel import SQLModel, Field as SQLModelField

# from pydantic import BaseModel, Field


class RawDataTable(SQLModel, table=True):
    """
    Tabla para almacenar los datos crudos utilizados en el modelo de regresión.

    Esta clase define la estructura de la tabla ``raw_data`` que contiene las
    características y variables objetivo necesarias para entrenar y validar el
    modelo de regresión.

    :param venta_id: Identificador único de la venta. Se genera automáticamente en la base de datos (autoincrementable).
    :type venta_id: Optional[int]
    :param metros_cuadrados: Área en metros cuadrados. Puede ser nulo.
    :type metros_cuadrados: Optional[float]
    :param num_habitaciones: Número de habitaciones. Puede ser nulo.
    :type num_habitaciones: Optional[int]
    :param ubicacion: Ubicación o dirección. Puede ser nulo.
    :type ubicacion: Optional[str]
    :param valor_venta: Valor de la venta. Es obligatorio y debe ser mayor que 0.
    :type valor_venta: float
    """
    __tablename__ = "raw_data"

    venta_id: Optional[int] = SQLModelField(default=None, primary_key=True, index=True)
    metros_cuadrados: Optional[float] = SQLModelField(nullable=True)
    num_habitaciones: Optional[float] = SQLModelField(nullable=True)
    ubicacion: Optional[str] = SQLModelField(default=None, nullable=True)
    valor_venta: float = SQLModelField(..., gt=0, nullable=False)
