from typing import List
from uuid import UUID
from pydantic import validator

from shared.utils.schemas_base import BaseSchema, DateTimeModelMixin, IDModelMixin 


class ProductBase(BaseSchema):
    product_name: str | None
    description: str | None
    price: float | None
    
    @validator("product_name")
    def product_name_must_have_more_than_three_characters(cls, v) -> str:
        if len(v) < 3:
            raise ValueError("El nombre del producto debe tener al menos 3 caracteres")
        return v
    
class ProductCreate(ProductBase):
    product_name: str 
    description: str 
    price: float 
    
    
class ProductToSave(ProductCreate):
    created_by: UUID | None
    updated_by: UUID | None
    

class ProductInDB(ProductBase, IDModelMixin, DateTimeModelMixin):
    is_active: bool | None
    created_by: UUID | str | None
    updated_by: UUID | str | None
    
    
class ProductToUpdate(ProductBase):
    is_active: bool | None