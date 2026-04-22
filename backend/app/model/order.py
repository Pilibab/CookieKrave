from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime

class OrderBase(BaseModel):
    """
        used for reading data from the data base
    """
    ORD_ID: int
    CUST_ID: int

    # This allows Pydantic to work with SQLAlchemy/SQLModel objects
    model_config = ConfigDict(from_attributes=True)

class Order(OrderBase):
    ORD_TIME: datetime
    total_amount: float
    ORD_PAY_METH: str = Field(min_length=5, max_length=64)
    ORD_F_TYPE: str = Field(min_length=5, max_length=64)


class OrderCreate(OrderBase):
    """Used when receiving data from the Frontend (ID isn't created yet)"""
    pass