from pydantic import BaseModel, ConfigDict

class CartBase(BaseModel):
    """
        used for reading data from the data base
    """
    ORD_ID:int
    PROD_ID:int

    # This allows Pydantic to work with SQLAlchemy/SQLModel objects
    model_config = ConfigDict(from_attributes=True)

class Cart(CartBase):
    CART_QUAN: int = 1


class CartCreate(CartBase):
    """Used when receiving data from the Frontend (ID isn't created yet)"""
    pass
