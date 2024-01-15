from databases import Database
from loguru import logger
from typing import List
from uuid import UUID

from modules.orders.orders_exceptions import OrdersExceptions
from modules.orders.orders_schemas import OrdersInDB, OrdersToSave, OrdersToUpdate
from shared.utils.record_to_dict import record_to_dict
import shared.utils.repository_utils as ru

class OrdersRepository:
    def __init__(self, db: Database):
        self.db = db
    
    async def create_orders(self, orders: OrdersToSave) -> OrdersInDB:
        from modules.orders.orders_sqlstatements import CREATE_ORDERS_ITEM
        
        values = ru.preprocess_create(orders.dict())
        record = await self.db.fetch_one(query=CREATE_ORDERS_ITEM, values=values)
        
        result = record_to_dict(record)
        
        return OrdersInDB(**result)
    
    
    
    
    async def get_orders_list(
        self,
        search: str | None,
        order: str | None,
        direction: str | None,
    ) -> List:
        from modules.orders.orders_sqlstatements import GET_ORDERS_LIST, orders_list_complements, orders_list_search
        

        order = order.lower() if order != None else None
        direction = direction.upper() if order != None else None
        values = {}
        sql_sentence = orders_list_complements(order, direction)
        sql_search = orders_list_search()

        if not search:
            sql_sentence = GET_ORDERS_LIST + sql_sentence
        else:
            sql_sentence = GET_ORDERS_LIST + sql_search + sql_sentence
            values["search"] = "%" + search + "%"

        records = await self.db.fetch_all(query=sql_sentence, values=values)

        if len(records) == 0 or not records:
            return []
        
        return [OrdersInDB(**dict(record)) for record in records] 
    
    
    
    
    
    async def get_orders_by_id(self, id: UUID) -> OrdersInDB | dict:
        from modules.orders.orders_sqlstatements import GET_ORDERS_BY_ID

        values = {"id": id}
        record = await self.db.fetch_one(query=GET_ORDERS_BY_ID, values=values)
        if not record:
            return {}

        orders = record_to_dict(record)
        return OrdersInDB(**orders)
    
    
    async def update_orders(
        self,
        id: UUID,
        orders_update: OrdersToUpdate,
        updated_by_id: UUID,
    ) -> OrdersInDB | dict:
        from modules.orders.orders_sqlstatements import UPDATE_ORDERS_BY_ID

        orders = await self.get_orders_by_id(id=id)
        if not orders:
            return {}

        orders_update_params = orders.copy(update=orders_update.dict(exclude_unset=True))

        orders_params_dict = orders_update_params.dict()
        orders_params_dict["updated_by"] = updated_by_id
        orders_params_dict["updated_at"] = ru._preprocess_date()
        
        try:
            record = await self.db.fetch_one(query=UPDATE_ORDERS_BY_ID, values=orders_params_dict)
            orders_updated = record_to_dict(record)
            return await self.get_orders_by_id(id=orders_updated.get("id"))
        except Exception as e:
            logger.error(f"Datos inválidos para actualizar una tarea: {e}")
            raise OrdersExceptions.OrdersInvalidUpdateParamsException()    
        
        
    async def delete_orders_by_id(
        self,
        id: UUID,
    ) -> UUID | dict:
        from modules.orders.orders_sqlstatements import DELETE_ORDERS_BY_ID

        orders = await self.get_orders_by_id(id=id)

        if not orders:
            return {}
        
        record = await self.db.fetch_one(query= DELETE_ORDERS_BY_ID, values = {"id": id})
        orders_id_delete = dict(record)        

        return orders_id_delete