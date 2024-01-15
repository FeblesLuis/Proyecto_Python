from uuid import UUID

from databases import Database
from loguru import logger

from shared.utils.verify_uuid import is_valid_uuid

from shared.utils.service_result import ServiceResult
from modules.product.product_exceptions import ProductExceptions
from modules.product.product_repositories import ProductRepository
from modules.product.product_schemas import ProductCreate, ProductInDB, ProductToSave, ProductToUpdate
from modules.users.users.user_schemas import UserInDB
from shared.utils.short_pagination import short_pagination
from shared.core.config import API_PREFIX

class ProductService:
    def __init__(self, db: Database):
        self.db = db
        
    async def create_product(self, product: ProductCreate, current_user: UserInDB):
        
        new_product = ProductToSave(**product.dict())
        new_product.created_by = current_user.id
        new_product.updated_by = current_user.id
        
        product_item = await ProductRepository(self.db).create_product(new_product) #se instacia de repositorio 
        if not product_item:
            logger.error("Error in DB creating a product")
            return ServiceResult(ProductExceptions.ProductCreateException())
        
        return ServiceResult(product_item)
    
   
    async def get_product_list(
        self,
        search: str | None,
        page_num: int = 1,
        page_size: int = 10,
        order: str = None,
        direction: str = None,
    ) -> ServiceResult:
        product = await ProductRepository(self.db).get_product_list(search, order, direction)
        
        service_result = None
        if len(product) == 0:
            service_Result = ServiceResult([])
            service_result.status_code = 204
        else:
            response = short_pagination(
                page_num=page_num,
                page_size=page_size,
                data_list=product,
                route=f"{API_PREFIX}/product",
            )
            service_result = ServiceResult(response)
            
        return service_result
    
    
    
    
    
    async def get_product_by_id(self, id: UUID) -> ServiceResult:
        product_in_db = await ProductRepository(self.db).get_product_by_id(id=id)

        if isinstance(product_in_db, dict) and not product_in_db.get("id"):
            logger.info("La tarea solicitada no está en base de datos")
            return ServiceResult(ProductExceptions.ProductNotFoundException())

        product = ProductInDB(**product_in_db.dict())
        return ServiceResult(product)
    
    
    async def update_product(
        self, id: UUID, product_update: ProductToUpdate, current_user: UserInDB
    ) -> ServiceResult:
        if not is_valid_uuid(id):
            return ServiceResult(ProductExceptions.ProductIdNoValidException())

        try:
            product = await ProductRepository(self.db).update_product(
                id=id,
                product_update=product_update,
                updated_by_id=current_user.id,
            )

            if isinstance(product, dict) and not product.get("id"):
                logger.info("El ID del producto a actualizar no está en base de datos")
                return ServiceResult(ProductExceptions.ProductNotFoundException())

            return ServiceResult(ProductInDB(**product.dict()))

        except Exception as e:
            logger.error(f"Se produjo un error: {e}")
            return ServiceResult(ProductExceptions.ProductInvalidUpdateParamsException(e))
        
        
        
    async def delete_product_by_id(
        self, id: UUID
    ) -> ServiceResult:
        
        product_id = await ProductRepository(self.db).delete_product_by_id(id=id)

        if isinstance(product_id, dict) and not product_id.get("id"):
            logger.info("El ID del producto a eliminar no está en base de datos")
            return ServiceResult(ProductExceptions.ProductNotFoundException())
        
        return  ServiceResult(product_id)