from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime

class InvoiceBase(BaseModel):
    """
        used for reading data from the data base
    """
    
    invoice_date: datetime
    bill_detail: str = Field(min_length=5, max_length=255)
    # This allows Pydantic to work with SQLAlchemy/SQLModel objects
    model_config = ConfigDict(from_attributes=True)

class Invoice(InvoiceBase):
    ORD_ID: int
    
class InvoiceCreate(InvoiceBase):
    """Used when receiving data from the Frontend (ID isn't created yet)"""
    pass
