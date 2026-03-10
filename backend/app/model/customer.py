from pydantic import BaseModel, ConfigDict, Field, EmailStr
from typing import Optional
from datetime import datetime

class CustomerBase(BaseModel):
    """
        used for reading data from the data base
    """
    customer_id: int
    created_at: datetime

    # This allows Pydantic to work with SQLAlchemy/SQLModel objects
    model_config = ConfigDict(from_attributes=True)

class Customer(CustomerBase):
        
    full_name: str = Field(min_length=5, max_length=255)
    email: EmailStr
    social_provider: Optional[str] = Field(None, pattern="^(google|facebook)$")
    social_id: Optional[str] = None
    contact_number: str = Field(..., max_length=20) # store in +63 format

class CustomerCreate(CustomerBase):
    """Used when receiving data from the Frontend (ID isn't created yet)"""
    pass
