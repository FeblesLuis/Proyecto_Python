from typing import Dict
from uuid import UUID

from databases import Database
from fastapi import APIRouter, Body, Depends, Path, status
from loguru import logger 

# from modules.orders.orders_services import OrdersService
from modules.orders.orders_services import OrdersService
from modules.orders.orders_schemas import OrdersCreate, OrdersInDB, OrdersToUpdate


from modules.users.users.user_schemas import UserInDB
from modules.users.auths.auth_dependencies import get_current_active_user
from modules.users.auths.auth_exceptions import AuthExceptions
from shared.core.db.db_dependencies import get_database
from shared.utils.service_result import ServiceResult, handle_result
from shared.utils.verify_auth import is_authorized

#Esto que está aquí es para manejar la documentación con el Swagger
orders_router = APIRouter(
    prefix="/orders",
    tags=["orders"],
    responses={404: {"description": "Not found"}},
)


#END POINTS:

#Orders: Create Orders
@orders_router.post(
    "/",
    response_model=OrdersInDB,
    name="orders:create-orders",
    status_code=status.HTTP_201_CREATED,
)
async def create_orders(
    orders: OrdersCreate = Body(..., embed=True), #Se crea el orders con los datos que se pasan en el body desde el request
    db: Database = Depends(get_database), #Inyeccion de dependencias
    current_user: UserInDB = Depends(get_current_active_user), #Verifica que el usuario esté autenticado para hacer uso de este endpoint
) -> ServiceResult:
    if not is_authorized(current_user, "orders:create-orders"): #verifica que el usuario tenga el permiso para hacer uso de este endpoint
        return handle_result(ServiceResult(AuthExceptions.AuthUnauthorizedException())) #sino devuelve una excepción
    
    result = await OrdersService(db).create_orders(orders, current_user)
    return handle_result(result)



@orders_router.get(
    "/",
    name="orders:orders_list",
    status_code=status.HTTP_200_OK
)
async def get_orders_list(
    search: str | None = None,
    page_number: int =1,
    page_size: int = 10,
    order: str = "",
    direction: str = "",
    db: Database = Depends(get_database),
    current_user: UserInDB = Depends(get_current_active_user),
) -> ServiceResult:
    if not is_authorized(current_user, "orders:get_orders_list"):
        return handle_result(ServiceResult(AuthExceptions.AuthUnauthorizedException()))
    
    result = await OrdersService(db).get_orders_list(
        search, page_num=page_number, page_size=page_size, order=order, direction=direction
    )
    return handle_result(result)







@orders_router.get(
    "/{id}", 
    response_model=Dict, 
    name="orders:get-orders-by-id")
async def get_orders_by_id(
    id: UUID = Path(..., title="The id of the orders to get"),
    db: Database = Depends(get_database),
    current_user: UserInDB = Depends(get_current_active_user),
) -> ServiceResult:
    if not is_authorized(current_user, "users:get-orders-by-id"):
        return handle_result(ServiceResult(AuthExceptions.AuthUnauthorizedException()))

    result = await OrdersService(db).get_orders_by_id(id=id)
    return handle_result(result)



@orders_router.put(
    "/{id}", 
    response_model=Dict, 
    name="orders:update-orders-by-id"
)
async def update_orders_by_id(
    id: UUID = Path(..., title="The id of the orders to update"),
    orders_update: OrdersToUpdate = Body(..., embed=True),
    db: Database = Depends(get_database),
    current_user: UserInDB = Depends(get_current_active_user),
) -> ServiceResult:
    if not is_authorized(current_user, "orders:update-orders-by-id"):
        return handle_result(ServiceResult(AuthExceptions.AuthUnauthorizedException()))

    result = await OrdersService(db).update_orders(
        id=id, orders_update=orders_update, current_user=current_user
    )
    return handle_result(result)





@orders_router.delete(
    "/{id}", 
    response_model=Dict, 
    name="orders:delete-orders-by-id"
)
async def delete_orders_by_id(
    id: UUID = Path(..., title="The id of the orders to update"),
    db: Database = Depends(get_database),
    current_user: UserInDB = Depends(get_current_active_user),
) -> ServiceResult:
    if not is_authorized(current_user, "orders:delete-orders-by-id"):
        return handle_result(ServiceResult(AuthExceptions.AuthUnauthorizedException()))

    result = await OrdersService(db).delete_orders_by_id(
        id=id
    )
    return handle_result(result)
