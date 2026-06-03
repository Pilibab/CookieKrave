from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
from uuid import UUID
from typing import Literal, Optional

class OrderBase(BaseModel):
    cust_id: UUID
    total_amount: float = Field(ge=0)
    payment_method: Literal["Cash", "GCash"] = "Cash"  # CHANGED: ord_pay_meth → payment_method (matches DB)
    order_status: Literal["Pending", "Confirmed", "Baking", "Out for Delivery", "For Pickup", "Completed", "Cancelled"] = "Pending"

class OrderCreate(OrderBase):
    """Frontend sends this — no id, no fulfillment, no completion time."""
    fulfillment_id: int  # CHANGED: Optional[int] = None → required int (always set by service before insert)

class Order(OrderBase):
    """Full DB record."""
    ord_id: int
    ord_time: datetime
    ord_fulfillment_time: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)

class OrderUpdate(BaseModel):
    """
    Used when patching an order from the frontend.
    """
    cust_id: Optional[UUID] = None
    total_amount: Optional[float] = Field(default=None, ge=0)
    payment_method: Optional[Literal["Cash", "GCash"]] = None  # CHANGED: ord_pay_meth → payment_method (matches DB)
    order_status: Optional[Literal[
        "Pending", "Confirmed", "Baking",
        "Out for Delivery", "For Pickup", "Completed", "Cancelled"
    ]] = None

    model_config = ConfigDict(from_attributes=True)