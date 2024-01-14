from typing import List
from uuid import UUID
from pydantic import validator

from shared.utils.schemas_base import BaseSchema, DateTimeModelMixin, IDModelMixin 


class InventoryBase(BaseSchema):
    inventory_name: str | None
    location_stock: str | None
    
    @validator("inventory_name")
    def inventory_name_must_have_more_than_three_characters(cls, v) -> str:
        if len(v) < 3:
            raise ValueError("El nombre de la tarea debe tener al menos 3 caracteres")
        return v
    
class InventoryCreate(InventoryBase):
    inventory_name: str 
    location_stock: str 
    
    
class InventoryToSave(InventoryCreate):
    created_by: UUID | None
    updated_by: UUID | None
    

class InventoryInDB(InventoryBase, IDModelMixin, DateTimeModelMixin):
    is_active: bool | None
    created_by: UUID | str | None
    updated_by: UUID | str | None
    
    
class InventoryToUpdate(InventoryBase):
    is_active: bool | None