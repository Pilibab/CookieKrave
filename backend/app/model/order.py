from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime

class OrderBase(BaseModel):
    """Shared fields: What the frontend sends to start an order."""
    CUST_ID: int
    TOTAL_AMOUNT: float = Field(ge=0)
    ORD_PAY_METH: str = Field(min_length=1, max_length=64) # e.g., 'GCash', 'Cash'
    ORD_F_TYPE: str = Field(min_length=1, max_length=64)   # e.g., 'Delivery', 'Pick_Up'

    model_config = ConfigDict(from_attributes=True)

class OrderCreate(OrderBase):
    """
    Used for POST. 
    Frontend sends the customer ID and payment details.
    """
    pass

class Order(OrderBase):
    """
    Used for GET. 
    The database adds the specific ID and the timestamp.
    """
    ORD_ID: int
    ORD_TIME: datetime