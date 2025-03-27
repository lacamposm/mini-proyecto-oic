# oic_model_server/services/raw_data_service.py
import os

import csv

import pandas as pd

from shapely.geometry import Point

from oic_model_server.core.database import engine

from oic_model_server.models.raw_data import HouseRawDataTable,HouseRawGeoData

from sqlmodel import Session, select


def load_house_raw_data_to_db(csv_path: str):
    """
    Carga datos crudos de casas desde un archivo CSV a la tabla houses_raw_data.

    Esta función lee el archivo CSV especificado por `csv_path`, procesa cada registro y
    lo inserta en la tabla `houses_raw_data` de la base de datos. Si un registro con el mismo
    ID ya existe, se omite la inserción para evitar duplicados.

    :param csv_path: Ruta del archivo CSV que contiene los datos crudos de casas.
    :type csv_path: str
    """
    if not os.path.exists(csv_path):
        print(f"⚠️ No se encontró el archivo CSV en {csv_path}")
        return None

    print(f"📥 Inicio de carga de datos desde {csv_path} 📥 ")

    insert_count = 0
    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        with Session(engine) as session:
            
            for row in reader:                
                house_id = row.get("id")
                existing = session.exec(
                    select(HouseRawDataTable).where(HouseRawDataTable.id == int(house_id))
                ).first() if house_id else None

                if not existing:
                    
                    house_data = HouseRawDataTable(
                        id=int(house_id) if house_id else None,
                        date=row.get("date") if row.get("date") else None,
                        price=float(row["price"]) if row.get("price") else None,
                        bedrooms=int(row["bedrooms"]) if row.get("bedrooms") else None,
                        bathrooms=float(row["bathrooms"]) if row.get("bathrooms") else None,
                        sqft_living=int(row["sqft_living"]) if row.get("sqft_living") else None,
                        sqft_lot=int(row["sqft_lot"]) if row.get("sqft_lot") else None,
                        floors=float(row["floors"]) if row.get("floors") else None,
                        waterfront=int(row["waterfront"]) if row.get("waterfront") else None,
                        view=int(row["view"]) if row.get("view") else None,
                        condition=int(row["condition"]) if row.get("condition") else None,
                        grade=int(row["grade"]) if row.get("grade") else None,
                        sqft_above=int(row["sqft_above"]) if row.get("sqft_above") else None,
                        sqft_basement=int(row["sqft_basement"]) if row.get("sqft_basement") else None,
                        yr_built=int(row["yr_built"]) if row.get("yr_built") else None,
                        yr_renovated=int(row["yr_renovated"]) if row.get("yr_renovated") else None,
                        zipcode=int(row["zipcode"]) if row.get("zipcode") else None,
                        lat=float(row["lat"]) if row.get("lat") else None,
                        long=float(row["long"]) if row.get("long") else None,
                        sqft_living15=int(row["sqft_living15"]) if row.get("sqft_living15") else None,
                        sqft_lot15=int(row["sqft_lot15"]) if row.get("sqft_lot15") else None
                    )
                    session.add(house_data)
                    insert_count += 1

            session.commit()

    print(f"✅ Proceso completado: Se insertaron {insert_count} registros nuevos en la tabla `houses_raw_data`.")


def load_geo_house_raw_data_to_db():
    """
    Actualiza la tabla geo_houses_raw_data en la base de datos a partir de los datos
    de houses_raw_data. Se extraen los campos `id`, `lat` y `long`, se genera la geometría
    en formato WKT con SRID=4326 y se inserta (o actualiza) cada registro en la tabla geográfica.
    Solo se contará como "nuevo" el registro si no existe previamente.
    """
    print("📥 Actualizando la tabla geo_houses_raw_data...")
    
    query = "SELECT id, lat, long FROM houses_raw_data;"
    df = pd.read_sql(query, engine)
    
    df["geometry"] = df.apply(
        lambda row: f"SRID=4326;{Point(row['long'], row['lat']).wkt}", axis=1
    )
    
    new_count = 0
    update_count = 0
    with Session(engine) as session:
        for _, row in df.iterrows():
            
            existing = session.exec(
                select(HouseRawGeoData).where(HouseRawGeoData.id == row["id"])
            ).first()
            if existing is None:
                
                geo_record = HouseRawGeoData(id=row["id"], geometry=row["geometry"])
                session.add(geo_record)
                new_count += 1
            else:
                if existing.geometry != row["geometry"]:
                    existing.geometry = row["geometry"]
                    session.add(existing)
                    update_count += 1
        session.commit()
    
    print(f"✅ La tabla geo_houses_raw_data ha sido actualizada. Registros nuevos insertados: {new_count}. Registros actualizados: {update_count}")


