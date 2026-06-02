from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
from typing import Optional

class GCashPaymentCreate(BaseModel):
    ord_id: int
    reference_no: str = Field(max_length=50)
    amount: float

class GCashPayment(GCashPaymentCreate):
    paid_at: datetime
    model_config = ConfigDict(from_attributes=True)

class GCashPaymentUpdate(BaseModel):
    """
    Used when receiving data from the Frontend to update an existing GCash record.
    Typically utilized for correcting manually typed receipt data or reference numbers.
    """
    # ord_id usually shouldn't change, but left optional for flexibility
    ord_id: Optional[int] = None
    
    # Keeps the exact column constraint from your database
    reference_no: Optional[str] = Field(default=None, max_length=50)
    
    # Added ge=0.0 safety guard so a bad patch request can't set a negative payment
    amount: Optional[float] = Field(default=None, ge=0.0)

    model_config = ConfigDict(from_attributes=True)