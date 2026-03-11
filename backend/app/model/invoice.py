from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime

class InvoiceBase(BaseModel):
    """
        used for reading data from the data base
    """
    Invoice_id: int
    order_id: int

    # This allows Pydantic to work with SQLAlchemy/SQLModel objects
    model_config = ConfigDict(from_attributes=True)

class Invoice(InvoiceBase):
    invoice_date: datetime
    bill_detail: str = Field(min_length=5, max_length=255)
    
class InvoiceCreate(InvoiceBase):
    """Used when receiving data from the Frontend (ID isn't created yet)"""
    pass
