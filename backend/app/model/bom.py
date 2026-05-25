from pydantic import BaseModel, ConfigDict, Field

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