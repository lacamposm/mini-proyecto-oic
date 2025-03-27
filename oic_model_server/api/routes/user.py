# oic_model_server/api/routes/user.py
from sqlmodel import Session

from fastapi import APIRouter, Depends

from oic_model_server.core.database import get_db

from oic_model_server.models.user import UserCreate, UserRead, UserUpdate

from oic_model_server.services.user_service import UserService


router = APIRouter()


@router.post("/", response_model=UserRead)
def create_user(request: UserCreate, db: Session = Depends(get_db)):
    """
    Endpoint para inscribir un nuevo usuario.
    """
    service = UserService(db)
    user_obj = service.create_user(request)
    user_dict = user_obj.model_dump()
    
    return UserRead.model_validate(user_dict)


@router.patch("/{user_id}", response_model=UserRead)
def update_user(user_id: str, update_data: UserUpdate, db: Session = Depends(get_db)):
    """
    Actualiza los datos de un usuario existente.
    """
    service = UserService(db)
    return service.update_user(user_id, update_data)


@router.delete("/{user_id}", response_model=dict)
def delete_user(user_id: str, db: Session = Depends(get_db)):
    """
    Elimina un usuario de la base de datos.
    """
    service = UserService(db)
    service.delete_user(user_id)
    return {"message": "Usuario eliminado con éxito"}
