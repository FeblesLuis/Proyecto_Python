from fastapi import APIRouter
from modules.users import users_router
from modules.inventory.inventory_routes import inventory_router

router = APIRouter()

router.include_router(users_router)
router.include_router(inventory_router)