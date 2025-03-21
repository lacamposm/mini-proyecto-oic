# oic_model_server/services/user_service.py
from sqlmodel import Session, select

from fastapi import HTTPException

from oic_model_server.models.user import UserTable, UserCreate


class UserService:
    """
    Servicio de usuario.

    Proporciona métodos para registrar un nuevo usuario y obtener su información.
    """

    def __init__(self, db: Session):
        """
        Inicializa el servicio con una sesión de base de datos.

        :param db: Sesión activa para interactuar con la base de datos.
        :type db: Session
        """
        self.db = db

    def create_user(self, request: UserCreate) -> UserTable:
        """
        Crea un nuevo usuario en la base de datos.

        Este método valida que no exista previamente un usuario con el mismo nombre.
        En caso de que exista, lanza una excepción HTTP con código 400.

        :param request: Objeto con la información necesaria para registrar un usuario.
        :type request: UserCreate
        :return: El usuario recién creado.
        :rtype: UserTable
        :raises HTTPException: Si ya existe un usuario con el nombre proporcionado.
        """
        existing_user = self.db.exec(
            select(UserTable).where(UserTable.user_name == request.user_name)
        ).first()

        if existing_user:
            raise HTTPException(status_code=400, detail="Ya existe un usuario con ese nombre.")

        new_user = UserTable(user_name=request.user_name)
        self.db.add(new_user)
        self.db.commit()
        self.db.refresh(new_user)

        return new_user
