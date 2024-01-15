from uuid import UUID

from databases import Database
from loguru import logger

from shared.utils.verify_uuid import is_valid_uuid

from shared.utils.service_result import ServiceResult
from modules.raw_material.raw_material_exceptions import Raw_materialExceptions
from modules.raw_material.raw_material_repositories import Raw_materialRepository
from modules.raw_material.raw_material_schemas import Raw_materialCreate, Raw_materialInDB, Raw_materialToSave, Raw_materialToUpdate
from modules.users.users.user_schemas import UserInDB
from shared.utils.short_pagination import short_pagination
from shared.core.config import API_PREFIX

class Raw_materialService:
    def __init__(self, db: Database):
        self.db = db
        
    async def create_raw_material(self, raw_material: Raw_materialCreate, current_user: UserInDB):
        
        new_raw_material = Raw_materialToSave(**raw_material.dict())
        new_raw_material.created_by = current_user.id
        new_raw_material.updated_by = current_user.id
        
        raw_material_item = await Raw_materialRepository(self.db).create_raw_material(new_raw_material) #se instacia de repositorio 
        if not raw_material_item:
            logger.error("Error in DB creating a raw_material")
            return ServiceResult(Raw_materialExceptions.Raw_materialCreateException())
        
        return ServiceResult(raw_material_item)
    
   
    async def get_raw_material_list(
        self,
        search: str | None,
        page_num: int = 1,
        page_size: int = 10,
        order: str = None,
        direction: str = None,
    ) -> ServiceResult:
        raw_material = await Raw_materialRepository(self.db).get_raw_material_list(search, order, direction)
        
        service_result = None
        if len(raw_material) == 0:
            service_Result = ServiceResult([])
            service_result.status_code = 204
        else:
            response = short_pagination(
                page_num=page_num,
                page_size=page_size,
                data_list=raw_material,
                route=f"{API_PREFIX}/raw_material",
            )
            service_result = ServiceResult(response)
            
        return service_result
    
    
    
    
    
    async def get_raw_material_by_id(self, id: UUID) -> ServiceResult:
        raw_material_in_db = await Raw_materialRepository(self.db).get_raw_material_by_id(id=id)

        if isinstance(raw_material_in_db, dict) and not raw_material_in_db.get("id"):
            logger.info("La tarea solicitada no está en base de datos")
            return ServiceResult(Raw_materialExceptions.Raw_materialNotFoundException())

        raw_material = Raw_materialInDB(**raw_material_in_db.dict())
        return ServiceResult(raw_material)
    
    
    async def update_raw_material(
        self, id: UUID, raw_material_update: Raw_materialToUpdate, current_user: UserInDB
    ) -> ServiceResult:
        if not is_valid_uuid(id):
            return ServiceResult(Raw_materialExceptions.Raw_materialIdNoValidException())

        try:
            raw_material = await Raw_materialRepository(self.db).update_raw_material(
                id=id,
                raw_material_update=raw_material_update,
                updated_by_id=current_user.id,
            )

            if isinstance(raw_material, dict) and not raw_material.get("id"):
                logger.info("El ID de tarea a actualizar no está en base de datos")
                return ServiceResult(Raw_materialExceptions.Raw_materialNotFoundException())

            return ServiceResult(Raw_materialInDB(**raw_material.dict()))

        except Exception as e:
            logger.error(f"Se produjo un error: {e}")
            return ServiceResult(Raw_materialExceptions.Raw_materialInvalidUpdateParamsException(e))
        
        
        
    async def delete_raw_material_by_id(
        self, id: UUID
    ) -> ServiceResult:
        
        raw_material_id = await Raw_materialRepository(self.db).delete_raw_material_by_id(id=id)

        if isinstance(raw_material_id, dict) and not raw_material_id.get("id"):
            logger.info("El ID de tarea a eliminar no está en base de datos")
            return ServiceResult(Raw_materialExceptions.Raw_materialNotFoundException())
        
        return  ServiceResult(raw_material_id)