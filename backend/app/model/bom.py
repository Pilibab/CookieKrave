from pydantic import BaseModel, ConfigDict


class BomBase(BaseModel):
    """
        used for reading data from the data base
    """
    BOM_ID: int
    PROD_ID: int
    INV_ID: int

    # This allows Pydantic to work with SQLAlchemy/SQLModel objects
    model_config = ConfigDict(from_attributes=True)

class Bom(BomBase):
    BOM_QUAN_REQ: float 

class BomCreate(BomBase):
    """Used when receiving data from the Frontend (ID isn't created yet)"""
    pass
