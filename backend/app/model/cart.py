from pydantic import BaseModel, ConfigDict

class CartBase(BaseModel):
    """
        used for reading data from the data base
    """
    ORD_ID:int
    PROD_ID:int
    CART_QUAN: int = 1


    # This allows Pydantic to work with SQLAlchemy/SQLModel objects
    model_config = ConfigDict(from_attributes=True)

class Cart(CartBase):
    """The final model returned by the Repository."""
    # Since CART has no separate SERIAL ID in your SQL, 
    # this might just stay as is!
    pass

class CartCreate(CartBase):
    """Used when receiving data from the Frontend (ID isn't created yet)"""
    pass
