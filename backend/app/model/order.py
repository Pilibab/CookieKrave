from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
from uuid import UUID
from typing import Literal, Optional

class OrderBase(BaseModel):
    cust_id: UUID
    total_amount: float = Field(ge=0)
    ord_pay_meth: Literal["Cash", "GCash"] = "Cash"
    order_status: Literal["Pending", "Confirmed", "Baking", "Out for Delivery", "For Pickup", "Completed", "Cancelled"] = "Pending"  # was missing = assignment

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


class OrderUpdate(BaseModel):
    """
    Used when patching an order from the frontend.
    Allows changing status, updating totals, or switching payment methods.
    """
    # UUIDs are sent as strings or UUID objects from the frontend
    cust_id: Optional[UUID] = None
    
    # Keeps your financial integrity constraint intact
    total_amount: Optional[float] = Field(default=None, ge=0)
    
    # Enforces exact choices so the database doesn't crash on a typo
    ord_pay_meth: Optional[Literal["Cash", "GCash"]] = None
    order_status: Optional[Literal[
        "Pending", "Confirmed", "Baking", 
        "Out for Delivery", "For Pickup", "Completed", "Cancelled"
    ]] = None

    model_config = ConfigDict(from_attributes=True)