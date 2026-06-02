from pydantic import BaseModel, ConfigDict, Field
from typing import Optional
import enum

class UnitType(str, enum.Enum):
    PCS = "pcs"
    ML = "ml"
    G = "g"
    KG = "kg"

class InventoryBase(BaseModel):
    inv_ing_name: str = Field(min_length=5, max_length=64)
    inv_stock: float = 0.0 
    # unit of measure
    inv_uom: UnitType                                               # ? maybe this should be a class of class UnitType(enum.Enum) 
                                                                    # ? where it can be any value of PCS = "pcs" ML ="ml" etc
                                                                    # if this we need to change the sql logic too 
    # reorder trigger
    inv_rt: int = 0                                        # ! this should not be less than 0

    # This allows Pydantic to work with SQLAlchemy/SQLModel objects
    model_config = ConfigDict(from_attributes=True)


class InventoryCreate(InventoryBase):
    pass

class Inventory(InventoryBase):
    inv_id: int 

class InventoryUpdate(BaseModel):
    """
    Used for partial updates (e.g., restocking, changing reorder thresholds).
    Every single field is optional, while maintaining safety thresholds.
    """
    inv_ing_name: Optional[str] = Field(default=None, min_length=5, max_length=64)
    inv_stock: Optional[float] = Field(default=None, ge=0.0) # Prevents hacking stock to negative values
    inv_uom: Optional[UnitType] = None
    inv_rt: Optional[int] = Field(default=None, ge=0) # Ensures updated trigger is still >= 0

    model_config = ConfigDict(from_attributes=True)