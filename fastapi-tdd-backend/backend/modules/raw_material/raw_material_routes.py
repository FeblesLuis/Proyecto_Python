from typing import Dict
from uuid import UUID

from databases import Database
from fastapi import APIRouter, Body, Depends, Path, status
from loguru import logger 

from modules.raw_material.raw_material_services import Raw_materialService
from modules.raw_material.raw_material_schemas import Raw_materialCreate, Raw_materialInDB, Raw_materialToUpdate


from modules.users.users.user_schemas import UserInDB
from modules.users.auths.auth_dependencies import get_current_active_user
from modules.users.auths.auth_exceptions import AuthExceptions
from shared.core.db.db_dependencies import get_database
from shared.utils.service_result import ServiceResult, handle_result
from shared.utils.verify_auth import is_authorized

#Esto que está aquí es para manejar la documentación con el Swagger
raw_material_router = APIRouter(
    prefix="/raw_material",
    tags=["raw_material"],
    responses={404: {"description": "Not found"}},
)


#END POINTS:

#Raw_material: Create Raw_material
@raw_material_router.post(
    "/",
    response_model=Raw_materialInDB,
    name="raw_material:create-raw_material",
    status_code=status.HTTP_201_CREATED,
)
async def create_raw_material(
    raw_material: Raw_materialCreate = Body(..., embed=True), #Se crea el raw_material con los datos que se pasan en el body desde el request
    db: Database = Depends(get_database), #Inyeccion de dependencias
    current_user: UserInDB = Depends(get_current_active_user), #Verifica que el usuario esté autenticado para hacer uso de este endpoint
) -> ServiceResult:
    if not is_authorized(current_user, "raw_material:create-raw_material"): #verifica que el usuario tenga el permiso para hacer uso de este endpoint
        return handle_result(ServiceResult(AuthExceptions.AuthUnauthorizedException())) #sino devuelve una excepción
    
    result = await Raw_materialService(db).create_raw_material(raw_material, current_user)
    return handle_result(result)



@raw_material_router.get(
    "/",
    name="raw_material:raw_material_list",
    status_code=status.HTTP_200_OK
)
async def get_raw_material_list(
    search: str | None = None,
    page_number: int =1,
    page_size: int = 10,
    order: str = "",
    direction: str = "",
    db: Database = Depends(get_database),
    current_user: UserInDB = Depends(get_current_active_user),
) -> ServiceResult:
    if not is_authorized(current_user, "raw_material:get_raw_material_list"):
        return handle_result(ServiceResult(AuthExceptions.AuthUnauthorizedException()))
    
    result = await Raw_materialService(db).get_raw_material_list(
        search, page_num=page_number, page_size=page_size, order=order, direction=direction
    )
    return handle_result(result)







@raw_material_router.get(
    "/{id}", 
    response_model=Dict, 
    name="raw_material:get-raw_material-by-id")
async def get_raw_material_by_id(
    id: UUID = Path(..., title="The id of the raw_material to get"),
    db: Database = Depends(get_database),
    current_user: UserInDB = Depends(get_current_active_user),
) -> ServiceResult:
    if not is_authorized(current_user, "users:get-raw_material-by-id"):
        return handle_result(ServiceResult(AuthExceptions.AuthUnauthorizedException()))

    result = await Raw_materialService(db).get_raw_material_by_id(id=id)
    return handle_result(result)



@raw_material_router.put(
    "/{id}", 
    response_model=Dict, 
    name="raw_material:update-raw_material-by-id"
)
async def update_raw_material_by_id(
    id: UUID = Path(..., title="The id of the raw_material to update"),
    raw_material_update: Raw_materialToUpdate = Body(..., embed=True),
    db: Database = Depends(get_database),
    current_user: UserInDB = Depends(get_current_active_user),
) -> ServiceResult:
    if not is_authorized(current_user, "raw_material:update-raw_material-by-id"):
        return handle_result(ServiceResult(AuthExceptions.AuthUnauthorizedException()))

    result = await Raw_materialService(db).update_raw_material(
        id=id, raw_material_update=raw_material_update, current_user=current_user
    )
    return handle_result(result)





@raw_material_router.delete(
    "/{id}", 
    response_model=Dict, 
    name="raw_material:delete-raw_material-by-id"
)
async def delete_raw_material_by_id(
    id: UUID = Path(..., title="The id of the raw_material to update"),
    db: Database = Depends(get_database),
    current_user: UserInDB = Depends(get_current_active_user),
) -> ServiceResult:
    if not is_authorized(current_user, "raw_material:delete-raw_material-by-id"):
        return handle_result(ServiceResult(AuthExceptions.AuthUnauthorizedException()))

    result = await Raw_materialService(db).delete_raw_material_by_id(
        id=id
    )
    return handle_result(result)
