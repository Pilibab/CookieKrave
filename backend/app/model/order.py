from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
from uuid import UUID
from typing import Literal

class OrderBase(BaseModel):
    """Shared fields: What the frontend sends to start an order."""
    cust_id: UUID
    total_amount: float = Field(ge=0)
    fulfillment_id: int
    ord_fulfillment_time: datetime
    ord_pay_meth: Literal["Cash", "GCash"] = "Cash"
    order_status = Literal["Pending", "Preparing", "Out for Delivery", "Completed", "Cancelled"]
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