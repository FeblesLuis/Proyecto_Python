from databases import Database
from loguru import logger
from typing import List
from uuid import UUID

from modules.inventory.inventory_exceptions import InventoryExceptions
from modules.inventory.inventory_schemas import InventoryInDB, InventoryToSave, InventoryToUpdate
from shared.utils.record_to_dict import record_to_dict
import shared.utils.repository_utils as ru

class InventoryRepository:
    def __init__(self, db: Database):
        self.db = db
    
    async def create_inventory(self, inventory: InventoryToSave) -> InventoryInDB:
        from modules.inventory.inventory_sqlstatements import CREATE_INVENTORY_ITEM
        
        values = ru.preprocess_create(inventory.dict())
        record = await self.db.fetch_one(query=CREATE_INVENTORY_ITEM, values=values)
        
        result = record_to_dict(record)
        
        return InventoryInDB(**result)
    
    
    
    
    async def get_inventory_list(
        self,
        search: str | None,
        order: str | None,
        direction: str | None,
    ) -> List:
        from modules.inventory.inventory_sqlstatements import GET_INVENTORY_LIST, inventory_list_complements, inventory_list_search
        

        order = order.lower() if order != None else None
        direction = direction.upper() if order != None else None
        values = {}
        sql_sentence = inventory_list_complements(order, direction)
        sql_search = inventory_list_search()

        if not search:
            sql_sentence = GET_INVENTORY_LIST + sql_sentence
        else:
            sql_sentence = GET_INVENTORY_LIST + sql_search + sql_sentence
            values["search"] = "%" + search + "%"

        records = await self.db.fetch_all(query=sql_sentence, values=values)

        if len(records) == 0 or not records:
            return []
        
        return [InventoryInDB(**dict(record)) for record in records] 
    
    
    
    
    
    async def get_inventory_by_id(self, id: UUID) -> InventoryInDB | dict:
        from modules.inventory.inventory_sqlstatements import GET_INVENTORY_BY_ID

        values = {"id": id}
        record = await self.db.fetch_one(query=GET_INVENTORY_BY_ID, values=values)
        if not record:
            return {}

        inventory = record_to_dict(record)
        return InventoryInDB(**inventory)
    
    
    async def update_inventory(
        self,
        id: UUID,
        inventory_update: InventoryToUpdate,
        updated_by_id: UUID,
    ) -> InventoryInDB | dict:
        from modules.inventory.inventory_sqlstatements import UPDATE_INVENTORY_BY_ID

        inventory = await self.get_inventory_by_id(id=id)
        if not inventory:
            return {}

        inventory_update_params = inventory.copy(update=inventory_update.dict(exclude_unset=True))

        inventory_params_dict = inventory_update_params.dict()
        inventory_params_dict["updated_by"] = updated_by_id
        inventory_params_dict["updated_at"] = ru._preprocess_date()
        
        try:
            record = await self.db.fetch_one(query=UPDATE_INVENTORY_BY_ID, values=inventory_params_dict)
            inventory_updated = record_to_dict(record)
            return await self.get_inventory_by_id(id=inventory_updated.get("id"))
        except Exception as e:
            logger.error(f"Datos inválidos para actualizar una tarea: {e}")
            raise InventoryExceptions.InventoryInvalidUpdateParamsException()    
        
        
    async def delete_inventory_by_id(
        self,
        id: UUID,
    ) -> UUID | dict:
        from modules.inventory.inventory_sqlstatements import DELETE_INVENTORY_BY_ID

        inventory = await self.get_inventory_by_id(id=id)

        if not inventory:
            return {}
        
        record = await self.db.fetch_one(query= DELETE_INVENTORY_BY_ID, values = {"id": id})
        inventory_id_delete = dict(record)        

        return inventory_id_delete