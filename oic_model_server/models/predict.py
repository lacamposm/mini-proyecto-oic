# oic_model_server/models/prediction.py
from sqlmodel import SQLModel, Field as SQLModelField

from sqlalchemy import ForeignKey, Column, JSON

from pydantic import BaseModel, Field, field_validator

from typing import Optional, Dict

from datetime import datetime


class PredictTable(SQLModel, table=True):
    """
    Representa un registro de predicción en la base de datos.
    
    Esta clase define la estructura para almacenar los datos de una predicción,
    incluyendo la información de las características en formato JSON, 
    el valor predicho y el usuario asociado.
    """
    __tablename__ = "predictions"
    
    predict_id: Optional[int] = SQLModelField(
        default=None, 
        primary_key=True
    )
    
    user_name: str = SQLModelField(
        sa_column=Column(
            ForeignKey(
                "users.user_name", 
                onupdate="CASCADE",
                ondelete="CASCADE",
            )
        )
    )
    
    feature_data: Dict = SQLModelField(
        sa_column=Column(JSON)
    )
    
    prediction: float = SQLModelField()
    
    created_at: datetime = SQLModelField(
        default_factory=datetime.now
    )


class HousePredictionRequest(BaseModel):
    """
    Modelo para la solicitud de predicción de precio de una inmueble.
    
    \f
    """
    user_name: str = Field(..., description="Nombre del usuario que realiza la solicitud")    
    bedrooms: Optional[int] = Field(None, ge=0, le=33, description="Número de habitaciones")
    bathrooms: Optional[float] = Field(None, ge=0.0, le=8.0, description="Número de baños")
    sqft_living: Optional[int] = Field(None, ge=290, le=13540, description="Pies cuadrados habitables")
    sqft_lot: Optional[int] = Field(None, ge=572, le=1651359, description="Tamaño del lote en pies cuadrados")
    floors: Optional[float] = Field(None, ge=1.0, le=3.5, description="Número de pisos")
    condition: Optional[int] = Field(None, ge=1, le=5, description="Condición general (1-5)")
    grade: Optional[int] = Field(None, ge=1, le=13, description="Calidad de construcción (1-13)")
    sqft_above: Optional[int] = Field(None, ge=290, le=9410, description="Pies cuadrados sobre el nivel del suelo")
    sqft_basement: Optional[int] = Field(None, ge=0, le=4820, description="Pies cuadrados del sótano")
    lat: Optional[float] = Field(None, ge=47.1559, le=47.7776, description="Latitud")
    long: Optional[float] = Field(None, ge=-122.515, le=-121.315, description="Longitud")
    renovated: Optional[int] = Field(None, ge=0, le=1, description="Indica si la propiedad fue renovada (0=No, 1=Sí)")
    
    waterfront: Optional[str] = Field(None, description="Propiedad frente al agua (0=No, 1=Sí)")
    view: Optional[str] = Field(None, description="Calidad de la vista (0-4)")
    zipcode: Optional[str] = Field(None, description="Código postal")

    @field_validator("waterfront")
    @classmethod
    def validate_waterfront(cls, v):
        if v is not None and v not in ["0", "1"]:
            raise ValueError('waterfront must be either "0" or "1"')
        return v

    @field_validator("view")
    @classmethod
    def validate_view(cls, v):
        if v is not None and v not in ["0", "1", "2", "3", "4"]:
            raise ValueError('view must be one of: "0", "1", "2", "3", "4"')
        return v

    @field_validator('zipcode')
    @classmethod
    def validate_zipcode(cls, v):
        valid_zipcodes = [
            "98038", "98001", "98106", "98074", "98034", "98023", "98092", "98144", 
            "98105", "98052", "98029", "98133", "98155", "98028", "98199", "98125", 
            "98004", "98118", "98042", "98045", "98002", "98103", "98027", "98055", 
            "98006", "98059", "98146", "98077", "98115", "98117", "98168", "98065", 
            "98039", "98058", "98056", "98122", "98053", "98072", "98136", "98005", 
            "98166", "98007", "98040", "98178", "98112", "98188", "98008", "98011", 
            "98075", "98033", "98031", "98116", "98109", "98003", "98107", "98022", 
            "98032", "98177", "98030", "98108", "98010", "98126", "98198", "98102", 
            "98019", "98119", "98014", "98148", "98024", "98070"
        ]
        if v is not None and v not in valid_zipcodes:
            raise ValueError(f"zipcode {v} not in the list of valid zipcodes")
        return v
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "user_name": "juan_perez",
                "bedrooms": 3,
                "bathrooms": 2.25,
                "sqft_living": 1800,
                "sqft_lot": 7200,
                "floors": 2.0,
                "waterfront": "0",
                "view": "0",
                "condition": 3,
                "grade": 8,
                "sqft_above": 1800,
                "sqft_basement": 0,
                "zipcode": "98052",
                "lat": 47.6307,
                "long": -122.0412,
                "renovated": 0
            }
        }
    }
    
    
class PredictionResponse(BaseModel):
    """
    Modelo de respuesta para representar una predicción guardada.
    
    Este modelo define la estructura de datos que se devuelve cuando se consultan
    las predicciones realizadas por un usuario específico.
    
    \f  
    """
    predict_id: int
    user_name: str
    prediction: float
    feature_data: Dict
    timestamp: Optional[datetime] = None
