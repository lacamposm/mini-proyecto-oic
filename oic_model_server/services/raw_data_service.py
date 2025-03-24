# oic_model_server/services/raw_data_service.py
import os

import csv

from oic_model_server.core.database import engine

from oic_model_server.models.raw_data import HouseRawDataTable

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
                    # Construir objeto para inserción con manejo adecuado de valores nulos
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
