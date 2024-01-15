from databases import Database
from loguru import logger
from typing import List
from uuid import UUID

from modules.product.product_exceptions import ProductExceptions
from modules.product.product_schemas import ProductInDB, ProductToSave, ProductToUpdate
from shared.utils.record_to_dict import record_to_dict
import shared.utils.repository_utils as ru

class ProductRepository:
    def __init__(self, db: Database):
        self.db = db
    
    async def create_product(self, product: ProductToSave) -> ProductInDB:
        from modules.product.product_sqlstatements import CREATE_PRODUCT_ITEM
        
        values = ru.preprocess_create(product.dict())
        record = await self.db.fetch_one(query=CREATE_PRODUCT_ITEM, values=values)
        
        result = record_to_dict(record)
        
        return ProductInDB(**result)
    
    
    
    
    async def get_product_list(
        self,
        search: str | None,
        order: str | None,
        direction: str | None,
    ) -> List:
        from modules.product.product_sqlstatements import GET_PRODUCT_LIST, product_list_complements, product_list_search
        

        order = order.lower() if order != None else None
        direction = direction.upper() if order != None else None
        values = {}
        sql_sentence = product_list_complements(order, direction)
        sql_search = product_list_search()

        if not search:
            sql_sentence = GET_PRODUCT_LIST + sql_sentence
        else:
            sql_sentence = GET_PRODUCT_LIST + sql_search + sql_sentence
            values["search"] = "%" + search + "%"

        records = await self.db.fetch_all(query=sql_sentence, values=values)

        if len(records) == 0 or not records:
            return []
        
        return [ProductInDB(**dict(record)) for record in records] 
    
    
    
    
    
    async def get_product_by_id(self, id: UUID) -> ProductInDB | dict:
        from modules.product.product_sqlstatements import GET_PRODUCT_BY_ID

        values = {"id": id}
        record = await self.db.fetch_one(query=GET_PRODUCT_BY_ID, values=values)
        if not record:
            return {}

        product = record_to_dict(record)
        return ProductInDB(**product)
    
    
    async def update_product(
        self,
        id: UUID,
        product_update: ProductToUpdate,
        updated_by_id: UUID,
    ) -> ProductInDB | dict:
        from modules.product.product_sqlstatements import UPDATE_PRODUCT_BY_ID

        product = await self.get_product_by_id(id=id)
        if not product:
            return {}

        product_update_params = product.copy(update=product_update.dict(exclude_unset=True))

        product_params_dict = product_update_params.dict()
        product_params_dict["updated_by"] = updated_by_id
        product_params_dict["updated_at"] = ru._preprocess_date()
        
        try:
            record = await self.db.fetch_one(query=UPDATE_PRODUCT_BY_ID, values=product_params_dict)
            product_updated = record_to_dict(record)
            return await self.get_product_by_id(id=product_updated.get("id"))
        except Exception as e:
            logger.error(f"Datos inválidos para actualizar una tarea: {e}")
            raise ProductExceptions.ProductInvalidUpdateParamsException()    
        
        
    async def delete_product_by_id(
        self,
        id: UUID,
    ) -> UUID | dict:
        from modules.product.product_sqlstatements import DELETE_PRODUCT_BY_ID

        product = await self.get_product_by_id(id=id)

        if not product:
            return {}
        
        record = await self.db.fetch_one(query= DELETE_PRODUCT_BY_ID, values = {"id": id})
        product_id_delete = dict(record)        

        return product_id_delete