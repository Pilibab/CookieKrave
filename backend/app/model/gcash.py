from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime

class GCashPaymentCreate(BaseModel):
    ord_id: int
    reference_no: str = Field(max_length=50)
    amount: float

class GCashPayment(GCashPaymentCreate):
    paid_at: datetime
    model_config = ConfigDict(from_attributes=True)