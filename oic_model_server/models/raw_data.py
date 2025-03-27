# oic_model_server/models/raw_data.py
from typing import Optional

from sqlmodel import SQLModel, Field as SQLModelField

from sqlalchemy import BigInteger, Column

from geoalchemy2 import Geometry

  

class HouseRawDataTable(SQLModel, table=True):
    """
    Tabla para almacenar los datos crudos de casas de King County.

    Esta clase define la estructura de la tabla ``houses_raw_data`` que contiene las
    características de las propiedades y sus precios de venta.

    :param id: Identificador único de la propiedad. Se genera automáticamente en la base de datos.
    :param date: Fecha de la venta. Puede ser nulo.
    :param price: Precio de venta de la propiedad en dólares. Debe ser mayor que 0.
    :param bedrooms: Número de dormitorios. Puede ser nulo.
    :param bathrooms: Número de baños (puede incluir decimales para baños parciales). Puede ser nulo.
    :param sqft_living: Superficie habitable en pies cuadrados. Puede ser nulo.
    :param sqft_lot: Superficie del terreno en pies cuadrados. Puede ser nulo.
    :param floors: Número de pisos (puede incluir decimales). Puede ser nulo.
    :param waterfront: Indica si la propiedad tiene vista al agua (1) o no (0). Puede ser nulo.
    :param view: Índice de calidad de la vista de la propiedad (0-4). Puede ser nulo.
    :param condition: Índice de condición general de la propiedad (1-5). Puede ser nulo.
    :param grade: Índice de calidad de construcción de la propiedad (1-13). Puede ser nulo.
    :param sqft_above: Superficie sobre el nivel del suelo en pies cuadrados. Puede ser nulo.
    :param sqft_basement: Superficie del sótano en pies cuadrados. Puede ser nulo.
    :param yr_built: Año de construcción de la propiedad. Puede ser nulo.
    :param yr_renovated: Año de la última renovación (0 si no se ha renovado). Puede ser nulo.
    :param zipcode: Código postal de la ubicación de la propiedad. Puede ser nulo.
    :param lat: Latitud geográfica. Puede ser nulo.
    :param long: Longitud geográfica. Puede ser nulo.
    :param sqft_living15: Superficie media habitable de las 15 propiedades más cercanas en pies cuadrados. Puede ser nulo.
    :param sqft_lot15: Superficie media de terreno de las 15 propiedades más cercanas en pies cuadrados. Puede ser nulo.
    """
    __tablename__ = "houses_raw_data"    
    
    
    id: Optional[int] = SQLModelField(
        default=None, 
        sa_column=Column(BigInteger, primary_key=True)
    )       
    price: Optional[float] = SQLModelField(gt=0, nullable=True)    
    date: Optional[str] = SQLModelField(default=None, nullable=True)   
    bedrooms: Optional[int] = SQLModelField(default=None, nullable=True)
    bathrooms: Optional[float] = SQLModelField(default=None, nullable=True)
    sqft_living: Optional[int] = SQLModelField(default=None, nullable=True)
    sqft_lot: Optional[int] = SQLModelField(default=None, nullable=True)
    floors: Optional[float] = SQLModelField(default=None, nullable=True)
    waterfront: Optional[int] = SQLModelField(default=None, nullable=True)
    view: Optional[int] = SQLModelField(default=None, nullable=True)
    condition: Optional[int] = SQLModelField(default=None, nullable=True)
    grade: Optional[int] = SQLModelField(default=None, nullable=True)
    sqft_above: Optional[int] = SQLModelField(default=None, nullable=True)
    sqft_basement: Optional[int] = SQLModelField(default=None, nullable=True)    
    yr_built: Optional[int] = SQLModelField(default=None, nullable=True)
    yr_renovated: Optional[int] = SQLModelField(default=None, nullable=True)    
    zipcode: Optional[int] = SQLModelField(default=None, nullable=True)
    lat: Optional[float] = SQLModelField(default=None, nullable=True)
    long: Optional[float] = SQLModelField(default=None, nullable=True)    
    sqft_living15: Optional[int] = SQLModelField(default=None, nullable=True)
    sqft_lot15: Optional[int] = SQLModelField(default=None, nullable=True)


class HouseRawGeoData(SQLModel, table=True):
    """
    Tabla para almacenar únicamente el identificador y la geometría (como POINT) de cada propiedad.
    Esta tabla se usará para operaciones geoespaciales y modelos ML que requieran información geográfica.
    """
    __tablename__ = "geo_houses_raw_data"
    
    id: Optional[int] = SQLModelField(
        default=None, 
        sa_column=Column(BigInteger, primary_key=True)
    ) 
    geometry: Optional[str] = SQLModelField(sa_column=Column(Geometry(geometry_type='POINT', srid=4326)))
