# model/utils.py
import os

import json

import pandas as pd

import geopandas as gpd

from dotenv import load_dotenv

from sqlalchemy import create_engine


load_dotenv()


def get_postgres_engine():
    """
    Crea y retorna una conexión (engine) a `PostgreSQL` usando `SQLAlchemy`.
    
    Utiliza la variable de entorno DATABASE_URL que debe contener la cadena de conexión
    completa a la base de datos PostgreSQL.

    :return: `SQLAlchemy` Engine conectado a `PostgreSQL`.
    :rtype: sqlalchemy.engine.Engine
    """
    DATABASE_URL = os.getenv("DATABASE_URL")
    return create_engine(DATABASE_URL)


def get_df_houses_data():
    """
    Obtiene los datos de houses_raw_data desde la base de datos `PostgreSQL`.

    :return: pd.DataFrame con los registros de houses_raw_data.
    :rtype: pandas.DataFrame
    """
    engine = get_postgres_engine()
    query = "SELECT * FROM houses_raw_data;"
    return pd.read_sql(query, engine)


def get_geo_df_houses_data():
    """
    Obtiene datos geoespaciales de casas.
    
    :return: GeoDataFrame con los datos geoespaciales de casas.
    :rtype: geopandas.GeoDataFrame
    """
    engine = get_postgres_engine()
    query = "SELECT id, geometry FROM geo_houses_raw_data;"
    
    return gpd.read_postgis(query, engine, geom_col="geometry")


def save_schema(X, path):
    """
    Guarda el esquema de datos de entrada en formato `JSON` con metadatos enriquecidos.
    
    Además de los tipos de datos, incluye:
    - Para variables categóricas: la lista de valores únicos posibles
    - Para variables numéricas: estadísticas descriptivas (min, max, media, desviación)
    
    Este esquema enriquecido permite validar nuevos datos y documentar la API
    adecuadamente, facilitando la detección de errores o valores fuera de rango.
    
    :param X: DataFrame de pandas cuyos metadatos se quieren guardar
    :type X: pandas.DataFrame
    :param path: Ruta del archivo donde se guardará el esquema `JSON`
    :type path: str
    :return: None
    """
    enriched_schema = {}
    
    for col, dtype in X.dtypes.items():
        col_info = {"dtype": str(dtype)}
        
        if pd.api.types.is_numeric_dtype(dtype):
            col_info.update({
                "min": float(X[col].min()),
                "max": float(X[col].max()),
                "mean": float(X[col].mean()),
                "std": float(X[col].std())
            })
        
        elif pd.api.types.is_object_dtype(dtype) or pd.api.types.is_categorical_dtype(dtype):
            
            unique_values = X[col].unique().tolist()
            col_info["unique_count"] = len(unique_values)
            col_info["sample_values"] = unique_values
                    
        elif pd.api.types.is_datetime64_dtype(dtype):
            col_info.update({
                "min_date": str(X[col].min()),
                "max_date": str(X[col].max())
            })
            
        enriched_schema[col] = col_info
    
    with open(path, "w") as f:
        json.dump(enriched_schema, f, indent=4)
    
    print(f"Archivo con esquema para la API guardado en: {path}")
