from pydantic import BaseModel, ConfigDict, Field
from typing import Optional
from decimal import Decimal
import enum

class UnitType(str, enum.Enum):
    PCS = "pcs"
    ML = "ml"
    G = "g"
    KG = "kg"

class InventoryBase(BaseModel):
    inv_ing_name: str = Field(min_length=1, max_length=64)
    # numeric(10, 3) -> maps to Decimal with 3 decimal places
    inv_stock: Decimal = Field(default=Decimal("0.000"), ge=0.0, decimal_places=3) 
    inv_uom: UnitType                                 
    # numeric(10, 2) -> maps to Decimal with 2 decimal places
    inv_rt: Decimal = Field(default=Decimal("0.00"), ge=0.0, decimal_places=2) 

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
    inv_stock: Optional[Decimal] = Field(default=None, ge=0.0, decimal_places=3) 
    inv_uom: Optional[UnitType] = None
    inv_rt: Optional[Decimal] = Field(default=None, ge=0.0, decimal_places=2) 

    model_config = ConfigDict(from_attributes=True)