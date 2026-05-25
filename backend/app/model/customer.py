from pydantic import BaseModel, ConfigDict, Field, EmailStr
from typing import Optional
from datetime import datetime
from uuid import UUID

class CustomerBase(BaseModel):
    """
        used for reading data from the data base
    """
    cust_cd: datetime
    cust_firstname: str = Field(min_length=5, max_length=85)
    cust_lastname: str = Field(min_length=5, max_length=85)
    cust_middlename: str = Field(max_length=85)
    cust_email: EmailStr
    cust_social_provider: Optional[str] = Field(None, pattern="^(google|facebook)$")
    cust_cont_no: str = Field(..., max_length=20) # store in +63 format

    # This allows Pydantic to work with SQLAlchemy/SQLModel objects
    model_config = ConfigDict(from_attributes=True)

class Customer(CustomerBase):
    cust_id: UUID
        


class CustomerCreate(CustomerBase):
    """Used when receiving data from the Frontend (ID isn't created yet)"""
    pass
