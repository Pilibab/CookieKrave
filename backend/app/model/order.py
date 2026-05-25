from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime

class OrderBase(BaseModel):
    """Shared fields: What the frontend sends to start an order."""
    cust_id: int
    total_amount: float = Field(ge=0)
    ord_pay_meth: str = Field(min_length=1, max_length=64) # e.g., 'GCash', 'Cash'
    ord_f_type: str = Field(min_length=1, max_length=64)   # e.g., 'Delivery', 'Pick_Up'

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
    ord_id: int
    ord_time: datetime