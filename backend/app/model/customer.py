from pydantic import BaseModel, ConfigDict, Field, EmailStr
from typing import Optional
from datetime import datetime

class CustomerBase(BaseModel):
    """
        used for reading data from the data base
    """
    CUST_CD: datetime
    CUST_FIRSTNAME: str = Field(min_length=5, max_length=85)
    CUST_LASTNAME: str = Field(min_length=5, max_length=85)
    CUST_MIDDLENAME: str = Field(max_length=85)
    CUST_EMAIL: EmailStr
    CUST_SOCIAL_PROVIDER: Optional[str] = Field(None, pattern="^(google|facebook)$")
    CUST_SOCIALID: Optional[str] = None
    CUST_CONT_NO: str = Field(..., max_length=20) # store in +63 format

    # This allows Pydantic to work with SQLAlchemy/SQLModel objects
    model_config = ConfigDict(from_attributes=True)

class Customer(CustomerBase):
    CUST_ID: int
        


class CustomerCreate(CustomerBase):
    """Used when receiving data from the Frontend (ID isn't created yet)"""
    pass
