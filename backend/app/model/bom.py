from pydantic import BaseModel, ConfigDict, Field

class BomBase(BaseModel):
    """Shared fields: Both the Frontend and DB need these."""
    PROD_ID: int
    INV_ID: int
    BOM_QUAN_REQ: float = Field(gt=0) # gt=0 matches your SQL CHECK constraint

    model_config = ConfigDict(from_attributes=True)

class BomCreate(BomBase):
    """Used for POST requests. Frontend sends PROD_ID, INV_ID, and QUAN."""
    pass

class Bom(BomBase):
    """Used for GET requests. Adds the DB-generated primary key."""
    BOM_ID: int