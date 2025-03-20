# oic_model_houses/models/prediction.py
from typing import Optional

from sqlmodel import SQLModel, Field


class PredictTable(SQLModel, table=True):
    """
    Representa un registro de predicción en la base de datos.

    Esta clase define la estructura para almacenar los datos de una predicción,
    incluyendo la información de las características y el valor predicho.
    """
    __tablename__ = "predictions"

    id: Optional[int] = Field(default=None, primary_key=True)
    feature_data: str = Field(...)
    prediction: float = Field(...)
