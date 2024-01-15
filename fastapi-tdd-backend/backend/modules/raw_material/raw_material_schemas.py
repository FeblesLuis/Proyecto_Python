from typing import List
from uuid import UUID
from pydantic import validator

from shared.utils.schemas_base import BaseSchema, DateTimeModelMixin, IDModelMixin 


class Raw_materialBase(BaseSchema):
    raw_material_name: str | None
    provider: str | None
    quantity: int | None
    
    @validator("raw_material_name")
    def raw_material_name_must_have_more_than_three_characters(cls, v) -> str:
        if len(v) < 3:
            raise ValueError("El nombre de la materia debe tener al menos 3 caracteres")
        return v
    
class Raw_materialCreate(Raw_materialBase):
    raw_material_name: str 
    provider: str 
    quantity: int
    
    
class Raw_materialToSave(Raw_materialCreate):
    created_by: UUID | None
    updated_by: UUID | None
    

class Raw_materialInDB(Raw_materialBase, IDModelMixin, DateTimeModelMixin):
    is_active: bool | None
    created_by: UUID | str | None
    updated_by: UUID | str | None
    
    
class Raw_materialToUpdate(Raw_materialBase):
    is_active: bool | None