from pydantic import BaseModel, ConfigDict, Field
from typing import List, Optional
from decimal import Decimal

class BomBase(BaseModel):
    prod_id: int
    inv_id: int
    bom_quan_req: Decimal = Field(gt=0, decimal_places=3) # Aligns with numeric(12,3) > 0

    model_config = ConfigDict(from_attributes=True)


class Bom(BomBase):
    """Returned when reading data from the DB (includes serial id)."""
    bom_id: int


class BomComponentCreate(BaseModel):
    """The shape of an item inside the creation list sent by the frontend."""
    inv_id: int
    bom_quan_req: Decimal = Field(gt=0, decimal_places=3)


class BomBulkCreate(BaseModel):
    """The master layout sent by the frontend to link multiple ingredients to a product."""
    prod_id: int
    ingredients: List[BomComponentCreate]


class BomUpdate(BaseModel):
    """Used for partial single row modifications later if needed."""
    prod_id: Optional[int] = None
    inv_id: Optional[int] = None
    bom_quan_req: Optional[Decimal] = Field(None, gt=0, decimal_places=3)

    model_config = ConfigDict(from_attributes=True)

class BomCreate(BomBase):
    """Retained to preserve generic signatures for your BaseRepository."""
    pass