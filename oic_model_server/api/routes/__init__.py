# oic_model_server/api/routes/__init__.py
from .user import router as user_router

from .predict import router as predict_router

__all__ = ["user_router", "predict_router"]
