# oic_model_houses/api/routes/user.py
from sqlmodel import Session

from fastapi import APIRouter, Depends

from oic_model_houses.core.database import get_db

from oic_model_houses.models.user import UserCreate, UserRead

from oic_model_houses.services.user_service import UserService


router = APIRouter()

@router.post("/", response_model=UserRead)
def inscribirse(request: UserCreate, db: Session = Depends(get_db)):
    """
    Endpoint para inscribir un nuevo usuario.
    """
    service = UserService(db)
    user_obj = service.create_user(request)
    user_dict = user_obj.model_dump()
    
    return UserRead.model_validate(user_dict)
