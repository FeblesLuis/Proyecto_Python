from uuid import UUID

from databases import Database
from loguru import logger

from shared.utils.verify_uuid import is_valid_uuid

from shared.utils.service_result import ServiceResult
from modules.orders.orders_exceptions import OrdersExceptions
from modules.orders.orders_repositories import OrdersRepository
from modules.orders.orders_schemas import OrdersCreate, OrdersInDB, OrdersToSave, OrdersToUpdate
from modules.users.users.user_schemas import UserInDB
from shared.utils.short_pagination import short_pagination
from shared.core.config import API_PREFIX

class OrdersService:
    def __init__(self, db: Database):
        self.db = db
        
    async def create_orders(self, orders: OrdersCreate, current_user: UserInDB):
        
        new_orders = OrdersToSave(**orders.dict())
        new_orders.created_by = current_user.id
        new_orders.updated_by = current_user.id
        
        orders_item = await OrdersRepository(self.db).create_orders(new_orders) #se instacia de repositorio 
        if not orders_item:
            logger.error("Error in DB creating a orders")
            return ServiceResult(OrdersExceptions.OrdersCreateException())
        
        return ServiceResult(orders_item)
    
   
    async def get_orders_list(
        self,
        search: str | None,
        page_num: int = 1,
        page_size: int = 10,
        order: str = None,
        direction: str = None,
    ) -> ServiceResult:
        orders = await OrdersRepository(self.db).get_orders_list(search, order, direction)
        
        service_result = None
        if len(orders) == 0:
            service_Result = ServiceResult([])
            service_result.status_code = 204
        else:
            response = short_pagination(
                page_num=page_num,
                page_size=page_size,
                data_list=orders,
                route=f"{API_PREFIX}/orders",
            )
            service_result = ServiceResult(response)
            
        return service_result
    
    
    
    
    
    async def get_orders_by_id(self, id: UUID) -> ServiceResult:
        orders_in_db = await OrdersRepository(self.db).get_orders_by_id(id=id)

        if isinstance(orders_in_db, dict) and not orders_in_db.get("id"):
            logger.info("La tarea solicitada no está en base de datos")
            return ServiceResult(OrdersExceptions.OrdersNotFoundException())

        orders = OrdersInDB(**orders_in_db.dict())
        return ServiceResult(orders)
    
    
    async def update_orders(
        self, id: UUID, orders_update: OrdersToUpdate, current_user: UserInDB
    ) -> ServiceResult:
        if not is_valid_uuid(id):
            return ServiceResult(OrdersExceptions.OrdersIdNoValidException())

        try:
            orders = await OrdersRepository(self.db).update_orders(
                id=id,
                orders_update=orders_update,
                updated_by_id=current_user.id,
            )

            if isinstance(orders, dict) and not orders.get("id"):
                logger.info("El ID de tarea a actualizar no está en base de datos")
                return ServiceResult(OrdersExceptions.OrdersNotFoundException())

            return ServiceResult(OrdersInDB(**orders.dict()))

        except Exception as e:
            logger.error(f"Se produjo un error: {e}")
            return ServiceResult(OrdersExceptions.OrdersInvalidUpdateParamsException(e))
        
        
        
    async def delete_orders_by_id(
        self, id: UUID
    ) -> ServiceResult:
        
        orders_id = await OrdersRepository(self.db).delete_orders_by_id(id=id)

        if isinstance(orders_id, dict) and not orders_id.get("id"):
            logger.info("El ID de tarea a eliminar no está en base de datos")
            return ServiceResult(OrdersExceptions.OrdersNotFoundException())
        
        return  ServiceResult(orders_id)