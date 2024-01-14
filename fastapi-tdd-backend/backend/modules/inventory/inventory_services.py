from uuid import UUID

from databases import Database
from loguru import logger

from shared.utils.verify_uuid import is_valid_uuid

from shared.utils.service_result import ServiceResult
from modules.inventory.inventory_exceptions import InventoryExceptions
from modules.inventory.inventory_repositories import InventoryRepository
from modules.inventory.inventory_schemas import InventoryCreate, InventoryInDB, InventoryToSave, InventoryToUpdate
from modules.users.users.user_schemas import UserInDB
from shared.utils.short_pagination import short_pagination
from shared.core.config import API_PREFIX

class InventoryService:
    def __init__(self, db: Database):
        self.db = db
        
    async def create_inventory(self, inventory: InventoryCreate, current_user: UserInDB):
        
        new_inventory = InventoryToSave(**inventory.dict())
        new_inventory.created_by = current_user.id
        new_inventory.updated_by = current_user.id
        
        inventory_item = await InventoryRepository(self.db).create_inventory(new_inventory) #se instacia de repositorio 
        if not inventory_item:
            logger.error("Error in DB creating a inventory")
            return ServiceResult(InventoryExceptions.InventoryCreateException())
        
        return ServiceResult(inventory_item)
    
   
    async def get_inventory_list(
        self,
        search: str | None,
        page_num: int = 1,
        page_size: int = 10,
        order: str = None,
        direction: str = None,
    ) -> ServiceResult:
        inventory = await InventoryRepository(self.db).get_inventory_list(search, order, direction)
        
        service_result = None
        if len(inventory) == 0:
            service_Result = ServiceResult([])
            service_result.status_code = 204
        else:
            response = short_pagination(
                page_num=page_num,
                page_size=page_size,
                data_list=inventory,
                route=f"{API_PREFIX}/inventory",
            )
            service_result = ServiceResult(response)
            
        return service_result
    
    
    
    
    
    async def get_inventory_by_id(self, id: UUID) -> ServiceResult:
        inventory_in_db = await InventoryRepository(self.db).get_inventory_by_id(id=id)

        if isinstance(inventory_in_db, dict) and not inventory_in_db.get("id"):
            logger.info("La tarea solicitada no está en base de datos")
            return ServiceResult(InventoryExceptions.InventoryNotFoundException())

        inventory = InventoryInDB(**inventory_in_db.dict())
        return ServiceResult(inventory)
    
    
    async def update_inventory(
        self, id: UUID, inventory_update: InventoryToUpdate, current_user: UserInDB
    ) -> ServiceResult:
        if not is_valid_uuid(id):
            return ServiceResult(InventoryExceptions.InventoryIdNoValidException())

        try:
            inventory = await InventoryRepository(self.db).update_inventory(
                id=id,
                inventory_update=inventory_update,
                updated_by_id=current_user.id,
            )

            if isinstance(inventory, dict) and not inventory.get("id"):
                logger.info("El ID de tarea a actualizar no está en base de datos")
                return ServiceResult(InventoryExceptions.InventoryNotFoundException())

            return ServiceResult(InventoryInDB(**inventory.dict()))

        except Exception as e:
            logger.error(f"Se produjo un error: {e}")
            return ServiceResult(InventoryExceptions.InventoryInvalidUpdateParamsException(e))
        
        
        
    async def delete_inventory_by_id(
        self, id: UUID
    ) -> ServiceResult:
        
        inventory_id = await InventoryRepository(self.db).delete_inventory_by_id(id=id)

        if isinstance(inventory_id, dict) and not inventory_id.get("id"):
            logger.info("El ID de tarea a eliminar no está en base de datos")
            return ServiceResult(InventoryExceptions.InventoryNotFoundException())
        
        return  ServiceResult(inventory_id)