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

    Esta función optimizada:
    1. Extrae primero los IDs únicos del CSV
    2. Compara con IDs existentes en la base de datos
    3. Solo procesa las filas del CSV que realmente necesitan ser insertadas

    Args:
        csv_path: Ruta del archivo CSV que contiene los datos crudos de casas.
    """
    if not os.path.exists(csv_path):
        print(f"⚠️ No se encontró el archivo CSV en {csv_path}")
        return None

    print(f"📥 Inicio de carga de datos desde: {csv_path} 📥... ")

    csv_ids = set()
    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row.get("id"):
                try:
                    csv_ids.add(int(row.get("id")))
                except (ValueError, TypeError):
                    pass
    
    if not csv_ids:
        print("⚠️ No se encontraron IDs válidos en el CSV")
        return

    with Session(engine) as session:
        existing_ids = set(session.exec(select(HouseRawDataTable.id)).all())
        ids_to_insert = csv_ids - existing_ids
        
        if not ids_to_insert:
            print("✅ Proceso completado: No hay nuevos registros para insertar.")
            return
        
        with open(csv_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            
            for row in reader:
                if not row.get("id"):
                    continue
                    
                try:
                    house_id = int(row.get("id"))
                    
                    existing = session.exec(
                        select(HouseRawDataTable.id).where(HouseRawDataTable.id == house_id)
                    ).first()
                    
                    if existing:
                        print(f"id de la casa repetido: {house_id}")
                        continue
                    
                    if house_id in ids_to_insert:

                        house_data = HouseRawDataTable(
                            id=house_id,
                            date=row.get("date"),
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
                        
                            
                except (ValueError, TypeError, KeyError) as e:
                    session.rollback()                    
                    print(f"⚠️ Error procesando fila con ID {row.get('id')}: {e}")
                    continue
            session.commit()
    print(f"✅ Proceso completado: Se insertaron {len(ids_to_insert)} registros nuevos en la tabla `houses_raw_data`.")



def load_geo_house_raw_data_to_db():
    """
    Actualiza la tabla geo_houses_raw_data en la base de datos de manera optimizada.
    
    Utiliza consultas SQLModel directas en lugar de pandas para mayor eficiencia.
    Procesa solo registros que realmente necesitan ser insertados o actualizados.
    """
    print("📥 Analizando datos para actualizar geo_houses_raw_data...")
    
    with Session(engine) as session:
         
        try:
            existing_geo_ids = set(session.exec(select(HouseRawGeoData.id)).all())
            raw_house_ids = set(session.exec(select(HouseRawDataTable.id)).all())
            
            new_ids = raw_house_ids - existing_geo_ids
            new_count = len(new_ids)
            
            insert_count = 0
            if new_ids:
                
                new_records = session.exec(
                    select(HouseRawDataTable).where(HouseRawDataTable.id.in_(new_ids))
                ).all()
                
                for record in new_records:
                    
                    insert_count += 1
                    if record.lat is not None and record.long is not None:
                        geometry = f"SRID=4326;{Point(record.long, record.lat).wkt}"
                        geo_record = HouseRawGeoData(id=record.id, geometry=geometry)
                        session.add(geo_record)                
            
                session.commit()
                
        except Exception as e:
            session.rollback()
            print(f"❌ Error al actualizar la tabla geo_houses_raw_data: {e}")
                
        print(f"✅ Tabla geo_houses_raw_data actualizada. Registros nuevos: {new_count}. Total registros: {len(existing_geo_ids)+insert_count}.")


