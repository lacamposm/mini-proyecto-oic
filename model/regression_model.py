# model/regression_model.py
import os

import pandas as pd

import geopandas as gpd

from pathlib import Path

from dotenv import load_dotenv

from shapely.geometry import Point

from sqlalchemy import create_engine

load_dotenv()


def get_postgres_engine():
    """
    Crea y retorna una conexión (engine) a `PostgreSQL` usando `SQLAlchemy`.

    :return: `SQLAlchemy` Engine conectado a `PostgreSQL`.
    """
    # user = os.getenv("POSTGRES_USER")
    # password = os.getenv("POSTGRES_PASSWORD")
    # host = os.getenv("POSTGRES_HOST")
    # port = os.getenv("POSTGRES_PORT")
    # database = os.getenv("POSTGRES_DB")
    
    # DATABASE_URL = f"postgresql://{user}:{password}@{host}:{port}/{database}"

    DATABASE_URL = os.getenv("DATABASE_URL")
    
    return create_engine(DATABASE_URL)


def get_geo_df_houses_data():
    """
    """
    engine = get_postgres_engine()
    query = "SELECT id, geometry FROM geo_houses_raw_data;"

    return gpd.read_postgis(query, engine, geom_col="geometry")



def get_df_houses_data():
    """
    Obtiene los datos de houses_raw_data desde la base de datos.

    :return: pd.DataFrame con los registros de houses_raw_data.
    """
    engine = get_postgres_engine()
    query = "SELECT * FROM houses_raw_data;"
    return pd.read_sql(query, engine)
