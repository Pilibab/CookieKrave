from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime

class OrderBase(BaseModel):
    """
        used for reading data from the data base
    """
    order_id: int
    customer_id: int

    # This allows Pydantic to work with SQLAlchemy/SQLModel objects
    model_config = ConfigDict(from_attributes=True)

class Order(OrderBase):
    order_time: datetime
    total_amount: float
    payment_method: str = Field(min_length=5, max_length=64)
    fullfillment_method: str = Field(min_length=5, max_length=64)


class OrderCreate(OrderBase):
    """Used when receiving data from the Frontend (ID isn't created yet)"""
    pass