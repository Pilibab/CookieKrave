from pydantic import BaseModel, ConfigDict, Field
from typing import Optional

class BomBase(BaseModel):
    """Shared fields: Both the Frontend and DB need these."""
    prod_id: int
    inv_id: int
    bom_quan_req: float = Field(gt=0) # gt=0 matches your SQL CHECK constraint

    model_config = ConfigDict(from_attributes=True)

class BomCreate(BomBase):
    """Used for POST requests. Frontend sends prod_id, inv_id, and bom_quan_req."""
    pass

class Bom(BomBase):
    """Used for GET requests. Adds the DB-generated primary key."""
    bom_id: int


class BomUpdate(BaseModel):
    """
    Used when receiving data from the Frontend to update an existing BOM record.
    All fields are completely optional to allow for flexible partial updates.
    """
    # All fields default to None, but we keep validation checks if they ARE sent
    prod_id: Optional[int] = None
    inv_id: Optional[int] = None
    bom_quan_req: Optional[float] = Field(default=None, gt=0)

    model_config = ConfigDict(from_attributes=True)