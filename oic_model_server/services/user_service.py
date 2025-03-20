# oic_model_server/services/user_service.py
from sqlmodel import Session, select

from fastapi import HTTPException

from oic_model_server.models.user import UserTable, UserCreate


class UserService:
    """
    Servicio de usuario.

    Proporciona métodos para inscribir un usuario y obtener la información del usuario.
    """
    def __init__(self, db: Session):
        """
        Initialize the ThreadService with a database session.

        :param db: The database session to use for interacting with the database.
        :type db: Session
        """
        self.db = db
    
    
    def create_user(self, request: UserCreate) -> UserTable:
        """
        Create a new user in the database.

        :param request: The request object containing the details for creating a new user.
        :type request: UserCreate
        :return: The newly created user.
        :rtype: UserTable
        :raises HTTPException: If a user with the given name already exists.
        """
        existing_user = self.db.exec(
            select(UserTable).where(UserTable.user_name == request.user_name)
        ).first()
        if existing_user:
            raise HTTPException(
                status_code=400, detail="User with given name already exists."
            )

        new_user = UserTable(user_name=request.user_name)
        self.db.add(new_user)
        self.db.commit()
        self.db.refresh(new_user)

        return new_user
