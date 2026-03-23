from fastapi import APIRouter
from app.api.endpoints import auth, users, items, categories, admin

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(items.router, prefix="/items", tags=["items"])
api_router.include_router(categories.router, prefix="/categories", tags=["categories"])
api_router.include_router(pickups.router, prefix="/pickups", tags=["pickups"])
api_router.include_router(admin.router, prefix="/admin", tags=["admin"])
api_router.include_router(agent.router, prefix="/agent", tags=["agent"])
api_router.include_router(center.router, prefix="/center", tags=["center"])
