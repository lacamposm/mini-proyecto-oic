# oic_model_server/core/config.py
import os

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Configuración de la aplicación usando BaseSettings de Pydantic.

    Esta clase define los parámetros de configuración para la aplicación,
    incluyendo el nombre del proyecto, la versión y la URL de conexión a la base de datos.

    :param PROJECT_NAME: El nombre del proyecto. Por defecto "Modelo Analitico OIC - API-SERVER".
    :type PROJECT_NAME: str
    :param PROJECT_VERSION: La versión del proyecto. Por defecto "0.1.0".
    :type PROJECT_VERSION: str
    :param DATABASE_URL: La URL para la conexión a la base de datos. Por defecto se usa una cadena de conexión para PostgreSQL.
    :type DATABASE_URL: str
    """

    PROJECT_NAME: str = "Modelo Analitico OIC - API-SERVER"
    PROJECT_VERSION: str = "0.1.0"
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "postgresql://postgres:postgres@oic-model-postgis:5432/postgres",
    )

settings = Settings()
