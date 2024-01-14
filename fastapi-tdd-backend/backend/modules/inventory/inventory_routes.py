from typing import Dict
from uuid import UUID

from databases import Database
from fastapi import APIRouter, Body, Depends, Path, status
from loguru import logger 

# from modules.inventory.inventory_services import InventoryService
from modules.inventory.inventory_services import InventoryService
from modules.inventory.inventory_schemas import InventoryCreate, InventoryInDB, InventoryToUpdate


from modules.users.users.user_schemas import UserInDB
from modules.users.auths.auth_dependencies import get_current_active_user
from modules.users.auths.auth_exceptions import AuthExceptions
from shared.core.db.db_dependencies import get_database
from shared.utils.service_result import ServiceResult, handle_result
from shared.utils.verify_auth import is_authorized

#Esto que está aquí es para manejar la documentación con el Swagger
inventory_router = APIRouter(
    prefix="/inventory",
    tags=["inventory"],
    responses={404: {"description": "Not found"}},
)


#END POINTS:

#Inventory: Create Inventory
@inventory_router.post(
    "/",
    response_model=InventoryInDB,
    name="inventory:create-inventory",
    status_code=status.HTTP_201_CREATED,
)
async def create_inventory(
    inventory: InventoryCreate = Body(..., embed=True), #Se crea el inventory con los datos que se pasan en el body desde el request
    db: Database = Depends(get_database), #Inyeccion de dependencias
    current_user: UserInDB = Depends(get_current_active_user), #Verifica que el usuario esté autenticado para hacer uso de este endpoint
) -> ServiceResult:
    if not is_authorized(current_user, "inventory:create-inventory"): #verifica que el usuario tenga el permiso para hacer uso de este endpoint
        return handle_result(ServiceResult(AuthExceptions.AuthUnauthorizedException())) #sino devuelve una excepción
    
    result = await InventoryService(db).create_inventory(inventory, current_user)
    return handle_result(result)



@inventory_router.get(
    "/",
    name="inventory:inventory_list",
    status_code=status.HTTP_200_OK
)
async def get_inventory_list(
    search: str | None = None,
    page_number: int =1,
    page_size: int = 10,
    order: str = "",
    direction: str = "",
    db: Database = Depends(get_database),
    current_user: UserInDB = Depends(get_current_active_user),
) -> ServiceResult:
    if not is_authorized(current_user, "inventory:get_inventory_list"):
        return handle_result(ServiceResult(AuthExceptions.AuthUnauthorizedException()))
    
    result = await InventoryService(db).get_inventory_list(
        search, page_num=page_number, page_size=page_size, order=order, direction=direction
    )
    return handle_result(result)







@inventory_router.get(
    "/{id}", 
    response_model=Dict, 
    name="inventory:get-inventory-by-id")
async def get_inventory_by_id(
    id: UUID = Path(..., title="The id of the inventory to get"),
    db: Database = Depends(get_database),
    current_user: UserInDB = Depends(get_current_active_user),
) -> ServiceResult:
    if not is_authorized(current_user, "users:get-inventory-by-id"):
        return handle_result(ServiceResult(AuthExceptions.AuthUnauthorizedException()))

    result = await InventoryService(db).get_inventory_by_id(id=id)
    return handle_result(result)



@inventory_router.put(
    "/{id}", 
    response_model=Dict, 
    name="inventory:update-inventory-by-id"
)
async def update_inventory_by_id(
    id: UUID = Path(..., title="The id of the inventory to update"),
    inventory_update: InventoryToUpdate = Body(..., embed=True),
    db: Database = Depends(get_database),
    current_user: UserInDB = Depends(get_current_active_user),
) -> ServiceResult:
    if not is_authorized(current_user, "inventory:update-inventory-by-id"):
        return handle_result(ServiceResult(AuthExceptions.AuthUnauthorizedException()))

    result = await InventoryService(db).update_inventory(
        id=id, inventory_update=inventory_update, current_user=current_user
    )
    return handle_result(result)





@inventory_router.delete(
    "/{id}", 
    response_model=Dict, 
    name="inventory:delete-inventory-by-id"
)
async def delete_inventory_by_id(
    id: UUID = Path(..., title="The id of the inventory to update"),
    db: Database = Depends(get_database),
    current_user: UserInDB = Depends(get_current_active_user),
) -> ServiceResult:
    if not is_authorized(current_user, "inventory:delete-inventory-by-id"):
        return handle_result(ServiceResult(AuthExceptions.AuthUnauthorizedException()))

    result = await InventoryService(db).delete_inventory_by_id(
        id=id
    )
    return handle_result(result)
