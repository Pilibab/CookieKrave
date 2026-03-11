from pydantic import BaseModel, ConfigDict


class BomBase(BaseModel):
    """
        used for reading data from the data base
    """
    Bom_id: int
    product_id: int
    inventory_id: int

    # This allows Pydantic to work with SQLAlchemy/SQLModel objects
    model_config = ConfigDict(from_attributes=True)

class Bom(BomBase):
    quantity_required: float 

class BomCreate(BomBase):
    """Used when receiving data from the Frontend (ID isn't created yet)"""
    pass
