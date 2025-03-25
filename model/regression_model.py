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


def load_or_create_geo_data():
    """
    Crea o carga la geo data de houses_raw_data.
    
    :return:  GeoDataFrame con la columna `id` y `geometry`.
    """
    shp_path = Path("data/geo/kc_houses_geo.shp")
    
    if shp_path.exists():
        gdf = gpd.read_file(str(shp_path))
    else:
        engine = get_postgres_engine()
        query = "SELECT * FROM houses_raw_data;"
        df_kc_houses = pd.read_sql(query, engine)
        geometry = [Point(xy) for xy in zip(df_kc_houses["long"], df_kc_houses["lat"])]
        gdf = gpd.GeoDataFrame(df_kc_houses, geometry=geometry, crs="EPSG:4326")[["id", "geometry"]]
        
        shp_path.parent.mkdir(parents=True, exist_ok=True)
        gdf.to_file(str(shp_path))
            
    return gdf


def get_df_houses_data():
    """
    Obtiene los datos de houses_raw_data desde la base de datos.

    :return: pd.DataFrame con los registros de houses_raw_data.
    """
    engine = get_postgres_engine()
    query = "SELECT * FROM houses_raw_data;"
    return pd.read_sql(query, engine)
