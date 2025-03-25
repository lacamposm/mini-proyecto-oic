# oic_model_server/main.py
import asyncio

from fastapi import FastAPI

from contextlib import asynccontextmanager

from sqlmodel import SQLModel

from oic_model_server.models import *

from oic_model_server.api.routes import user_router, predict_router

from oic_model_server.core.database import engine

from oic_model_server.services.raw_data_service import load_house_raw_data_to_db, load_geo_house_raw_data_to_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Gestiona el ciclo de vida de la aplicación.

    Este administrador de contexto se utiliza para manejar los eventos de inicio y 
    apagado de la aplicación FastAPI. Se asegura de que las tablas de la base de datos 
    se creen al iniciar la aplicación y muestra un mensaje cuando la aplicación se está apagando.

    :param app: La instancia de la aplicación FastAPI.
    :type app: FastAPI
    :yield: Control de vuelta a la aplicación hasta el apagado.
    """
    SQLModel.metadata.create_all(bind=engine)

    try:
        load_house_raw_data_to_db("kc_house_data.csv")
        load_geo_house_raw_data_to_db()
    except Exception as e:
            print(f"❌ Error al cargar datos desde el CSV o al generar la GeoData: {e}")
            
    try:
        load_geo_house_raw_data_to_db()
    except Exception as e:
            print(f"❌ Error al cargar datos Geograficos: {e}")

    print("🚀 ¡OIC-MODEL-API está en funcionamiento!🚀")
    await asyncio.sleep(0)
    yield
    print("🚧 La API se está apagando... 🛑")


def create_application() -> FastAPI:
    """
    Crea y configura la aplicación FastAPI.

    Se establece el título, la versión y la descripción de la API. Además, se incluye el router
    de usuario y se define el evento de startup para la creación de tablas en la base de datos.

    :return: Instancia de la aplicación FastAPI.
    :rtype: FastAPI
    """
    app = FastAPI(
        title="Modelo Analitico OIC - API-SERVER",
        version="0.1.0",
        description="API para predecir precios de casas, almacenar predicciones, etc.",
        lifespan=lifespan
    )

    app.include_router(user_router, prefix="/users", tags=["users"])
    app.include_router(predict_router, prefix="/predict", tags=["predict"])

    return app

app = create_application()


@app.get("/health")
def health_check():
    """
    Este endpoint devuelve una respuesta JSON simple para indicar que la API está operativa.
    """
    return {"status": "ok"}
