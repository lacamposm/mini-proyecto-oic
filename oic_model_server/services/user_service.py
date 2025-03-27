# oic_model_server/services/user_service.py
from sqlmodel import Session, select

from fastapi import HTTPException

from oic_model_server.models.user import UserTable, UserCreate, UserUpdate


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
        
        \t

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

    
    def update_user(self, user_id: str, update_data: UserUpdate) -> UserTable:
        """
        Actualiza los datos de un usuario existente.
        
        Este método busca un usuario por su ID y actualiza su nombre de usuario,
        si el nuevo nombre está disponible.
        
        \t        
        """
        user = self.db.get(UserTable, user_id)
        if not user:
            raise HTTPException(status_code=404, detail=f"Usuario con ID '{user_id}' no encontrado")
            
        if update_data.user_name and update_data.user_name != user.user_name:
            existing = self.db.exec(
                select(UserTable).where(UserTable.user_name == update_data.user_name)
            ).first()
            
            if existing:
                raise HTTPException(status_code=400, detail=f"El nombre de usuario '{update_data.user_name}' ya está en uso")
            
            user.user_name = update_data.user_name
            
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        
        return user
    
    def delete_user(self, user_id: str) -> bool:
        """
        Elimina un usuario de la base de datos y todas sus predicciones asociadas.
        
        Este método primero elimina todas las predicciones asociadas al usuario
        y luego elimina el usuario en sí, manteniendo la integridad referencial.
        \t
        """
        user = self.db.get(UserTable, user_id)
        if not user:
            raise HTTPException(status_code=404, detail=f"Usuario con ID '{user_id}' no encontrado")
        
        from oic_model_server.models.predict import PredictTable
        
        predictions = self.db.exec(
            select(PredictTable).where(PredictTable.user_name == user.user_name)
        ).all()
        
        for prediction in predictions:
            self.db.delete(prediction)
        
        self.db.delete(user)
        self.db.commit()
        
        return True
