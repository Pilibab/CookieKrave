from pydantic import BaseModel, ConfigDict

class CartBase(BaseModel):
    """
        used for reading data from the data base
    """
    order_id:int
    product_id:int

    # This allows Pydantic to work with SQLAlchemy/SQLModel objects
    model_config = ConfigDict(from_attributes=True)

class Cart(CartBase):
    quantity: int = 1
    price_per_item: float 

class CartCreate(CartBase):
    """Used when receiving data from the Frontend (ID isn't created yet)"""
    pass
