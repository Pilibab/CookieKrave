from pydantic import BaseModel, ConfigDict, Field

import enum

class UnitType(str, enum.Enum):
    PCS = "pcs"
    ML = "ml"
    G = "g"
    KG = "kg"

class InventoryBase(BaseModel):
    INV_ING_NAME: str = Field(min_length=5, max_length=64)
    INV_STOCK: float = 0.0 
    # unit of measure
    INV_UOM: UnitType                                               # ? maybe this should be a class of class UnitType(enum.Enum) 
                                                                    # ? where it can be any value of PCS = "pcs" ML ="ml" etc
                                                                    # if this we need to change the sql logic too 
    # reorder trigger
    INV_RT: int = 0                                        # ! this should not be less than 0

    # This allows Pydantic to work with SQLAlchemy/SQLModel objects
    model_config = ConfigDict(from_attributes=True)


class InventoryCreate(InventoryBase):
    pass

class Inventory(InventoryBase):
    INV_ID: int 

