from typing import List
from uuid import UUID
from pydantic import validator

from shared.utils.schemas_base import BaseSchema, DateTimeModelMixin, IDModelMixin 


class OrdersBase(BaseSchema):
    orders_name: str | None
    state: str | None
    
    @validator("orders_name")
    def orders_name_must_have_more_than_three_characters(cls, v) -> str:
        if len(v) < 3:
            raise ValueError("El nombre de la tarea debe tener al menos 3 caracteres")
        return v
    
class OrdersCreate(OrdersBase):
    orders_name: str 
    state: str 
    
    
class OrdersToSave(OrdersCreate):
    created_by: UUID | None
    updated_by: UUID | None
    

class OrdersInDB(OrdersBase, IDModelMixin, DateTimeModelMixin):
    is_active: bool | None
    created_by: UUID | str | None
    updated_by: UUID | str | None
    
    
class OrdersToUpdate(OrdersBase):
    is_active: bool | None