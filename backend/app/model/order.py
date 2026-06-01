from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
from uuid import UUID
from typing import Literal, Optional

class OrderBase(BaseModel):
    cust_id: UUID
    total_amount: float = Field(ge=0)
    ord_pay_meth: Literal["Cash", "GCash"] = "Cash"
    order_status: Literal["Pending", "Preparing", "Out for Delivery", "Completed", "Cancelled"] = "Pending"  # was missing = assignment

class OrderCreate(OrderBase):
    """Frontend sends this — no id, no fulfillment, no completion time."""
    ord_f_type: str  # fulfillment type needed to create fulfillment record
    fulfillment_id: Optional[int] = None        # set after fulfillment created


class Order(OrderBase):
    """Full DB record."""
    ord_id: int
    ord_time: datetime
    ord_fulfillment_time: Optional[datetime] = None  # only set on completion

    model_config = ConfigDict(from_attributes=True)