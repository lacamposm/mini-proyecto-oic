# oic_model_server/models/user.py
import uuid

from datetime import datetime

from sqlmodel import SQLModel, Field as SQLModelField

from pydantic import BaseModel, Field


class UserTable(SQLModel, table=True):
    """
    Representa un usuario en la base de datos.

    Esta clase define la estructura de la tabla ``users`` con los siguientes campos:

    - `user_id`: Identificador único del usuario.
    - `user_name`: Nombre de usuario único.
    - `created_at`: Fecha y hora de creación del registro.
    - `updated_at`: Fecha y hora de la última actualización.

    :param str user_id: Identificador único generado automáticamente.
    :param str user_name: Nombre de usuario único.
    :param datetime created_at: Fecha y hora de creación, generada automáticamente.
    :param datetime updated_at: Fecha y hora de la última actualización, generada automáticamente.
    """
    __tablename__ = "users"

    user_id: str = SQLModelField(
        default_factory=lambda: str(uuid.uuid4()),
        primary_key=True,
        nullable=False
    )
    user_name: str = SQLModelField(
        nullable=False,
        index=True,
        unique=True
    )
    created_at: datetime = SQLModelField(
        default_factory=datetime.now,
        nullable=False
    )
    updated_at: datetime = SQLModelField(
        default_factory=datetime.now,
        nullable=False
    )

class UserCreate(BaseModel):
    """
    Modelo Pydantic para la creación (inscripción) de un usuario.

    Este modelo se utiliza para validar los datos de entrada al registrar un nuevo usuario.
    Se requiere únicamente el campo ``user_name``, ya que el identificador y las marcas de
    tiempo se generan internamente en el servidor.

    :param user_name: Nombre de usuario único.
    :type user_name: str
    """
    user_name: str = Field(..., description="Nombre de usuario único.")

class UserRead(BaseModel):
    """
    Modelo Pydantic para la lectura de datos del usuario.

    Este modelo se utiliza para serializar la información del usuario que se devuelve al cliente.
    Se exponen únicamente los campos ``user_id`` y ``user_name`` para mantener interna la
    información de las marcas de tiempo.

    :param user_id: Identificador interno único.
    :type user_id: str
    :param user_name: Nombre de usuario único.
    :type user_name: str
    """
    user_id: str = Field(..., description="Identificador interno único")
    user_name: str = Field(..., description="Nombre de usuario único")

    model_config = {
        "from_attributes": True
    }
