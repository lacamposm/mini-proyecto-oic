# oic_model_server/services/raw_data_service.py
import os

import csv

from oic_model_server.core.database import engine

from oic_model_server.models.raw_data import RawDataTable

from sqlmodel import Session, select


def load_raw_data_to_db(csv_path: str):
    """
    Carga datos crudos desde un archivo CSV a la base de datos.

    Esta función lee el archivo CSV especificado por `csv_path`, procesa cada registro y
    lo inserta en la tabla `raw_data` de la base de datos. Si un registro con el mismo
    valor en el campo `venta_id` ya existe, se omite la inserción para evitar duplicados.

    :param csv_path: Ruta del archivo CSV que contiene los datos crudos.
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
                venta_id = row.get("venta_id")
                existing = session.exec(
                    select(RawDataTable).where(RawDataTable.venta_id == int(venta_id))
                ).first() if venta_id else None

                if not existing:
                    raw_data = RawDataTable(
                        venta_id=int(venta_id),
                        metros_cuadrados=float(row["metros_cuadrados"]) if row.get("metros_cuadrados") else None,
                        num_habitaciones=float(row["num_habitaciones"]) if row.get("num_habitaciones") else None,
                        ubicacion=row.get("ubicacion"),
                        valor_venta=float(row["valor_venta"]) if row.get("valor_venta") else None
                    )
                    session.add(raw_data)
                    insert_count += 1

            session.commit()

    print(f"✅ Proceso completado: Se insertaron {insert_count} registros nuevos en la tabla `raw_data`.")
