# oic_model_houses/core/database.py
from sqlmodel import Session, create_engine

from oic_model_houses.core.config import settings

from sqlalchemy.orm import sessionmaker

engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Session:
    """
    Proporciona una sesión de base de datos.

    Esta función crea una nueva sesión de base de datos y la cede al llamador.
    La sesión se cierra automáticamente cuando se termina de utilizar.

    :yield: Una nueva sesión de base de datos.
    :rtype: Session
    """
    with Session(engine) as session:
        yield session
