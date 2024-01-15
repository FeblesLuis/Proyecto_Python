from databases import Database
from loguru import logger
from typing import List
from uuid import UUID

from modules.raw_material.raw_material_exceptions import Raw_materialExceptions
from modules.raw_material.raw_material_schemas import Raw_materialInDB, Raw_materialToSave, Raw_materialToUpdate
from shared.utils.record_to_dict import record_to_dict
import shared.utils.repository_utils as ru

class Raw_materialRepository:
    def __init__(self, db: Database):
        self.db = db
    
    async def create_raw_material(self, raw_material: Raw_materialToSave) -> Raw_materialInDB:
        from modules.raw_material.raw_material_sqlstatements import CREATE_RAW_MATERIAL_ITEM
        
        values = ru.preprocess_create(raw_material.dict())
        record = await self.db.fetch_one(query=CREATE_RAW_MATERIAL_ITEM, values=values)
        
        result = record_to_dict(record)
        
        return Raw_materialInDB(**result)
    
    
    
    
    async def get_raw_material_list(
        self,
        search: str | None,
        order: str | None,
        direction: str | None,
    ) -> List:
        from modules.raw_material.raw_material_sqlstatements import GET_RAW_MATERIAL_LIST, raw_material_list_complements, raw_material_list_search
        

        order = order.lower() if order != None else None
        direction = direction.upper() if order != None else None
        values = {}
        sql_sentence = raw_material_list_complements(order, direction)
        sql_search = raw_material_list_search()

        if not search:
            sql_sentence = GET_RAW_MATERIAL_LIST + sql_sentence
        else:
            sql_sentence = GET_RAW_MATERIAL_LIST + sql_search + sql_sentence
            values["search"] = "%" + search + "%"

        records = await self.db.fetch_all(query=sql_sentence, values=values)

        if len(records) == 0 or not records:
            return []
        
        return [Raw_materialInDB(**dict(record)) for record in records] 
    
    
    
    
    
    async def get_raw_material_by_id(self, id: UUID) -> Raw_materialInDB | dict:
        from modules.raw_material.raw_material_sqlstatements import GET_RAW_MATERIAL_BY_ID

        values = {"id": id}
        record = await self.db.fetch_one(query=GET_RAW_MATERIAL_BY_ID, values=values)
        if not record:
            return {}

        raw_material = record_to_dict(record)
        return Raw_materialInDB(**raw_material)
    
    
    async def update_raw_material(
        self,
        id: UUID,
        raw_material_update: Raw_materialToUpdate,
        updated_by_id: UUID,
    ) -> Raw_materialInDB | dict:
        from modules.raw_material.raw_material_sqlstatements import UPDATE_RAW_MATERIAL_BY_ID

        raw_material = await self.get_raw_material_by_id(id=id)
        if not raw_material:
            return {}

        raw_material_update_params = raw_material.copy(update=raw_material_update.dict(exclude_unset=True))

        raw_material_params_dict = raw_material_update_params.dict()
        raw_material_params_dict["updated_by"] = updated_by_id
        raw_material_params_dict["updated_at"] = ru._preprocess_date()
        
        try:
            record = await self.db.fetch_one(query=UPDATE_RAW_MATERIAL_BY_ID, values=raw_material_params_dict)
            raw_material_updated = record_to_dict(record)
            return await self.get_raw_material_by_id(id=raw_material_updated.get("id"))
        except Exception as e:
            logger.error(f"Datos inválidos para actualizar una tarea: {e}")
            raise Raw_materialExceptions.Raw_materialInvalidUpdateParamsException()    
        
        
    async def delete_raw_material_by_id(
        self,
        id: UUID,
    ) -> UUID | dict:
        from modules.raw_material.raw_material_sqlstatements import DELETE_RAW_MATERIAL_BY_ID

        raw_material = await self.get_raw_material_by_id(id=id)

        if not raw_material:
            return {}
        
        record = await self.db.fetch_one(query= DELETE_RAW_MATERIAL_BY_ID, values = {"id": id})
        raw_material_id_delete = dict(record)        

        return raw_material_id_delete