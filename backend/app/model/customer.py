from pydantic import BaseModel, ConfigDict, Field, EmailStr
from typing import Optional
from datetime import datetime
from uuid import UUID

class CustomerBase(BaseModel):
    """
    Base fields shared across reading, creating, and updating customers.
    """
    cust_id: UUID  # FIX: Moved here if generated automatically by the DB
    cust_firstname: str = Field(max_length=85)
    cust_lastname: str = Field(max_length=85)
    cust_middlename: Optional[str] = Field(default=None, max_length=85)
    cust_email: EmailStr
    cust_social_provider: Optional[str] = Field(default=None, pattern="^(google|facebook)$")
    
    # FIX: Changed '...' to 'default=None' so the frontend can completely omit this key safely
    cust_cont_no: Optional[str] = Field(default=None, max_length=20) 

    model_config = ConfigDict(from_attributes=True)


class CustomerCreate(CustomerBase):
    """Used when receiving data from the Frontend (ID and creation date don't exist yet)"""
    pass


class CustomerUpdate(BaseModel):
    """
    Used for partial updates. Every single field is optional,
    preserving exact string lengths and regex pattern matching rules.
    """
    cust_firstname: Optional[str] = Field(default=None, max_length=85)
    cust_lastname: Optional[str] = Field(default=None, max_length=85)
    cust_middlename: Optional[str] = Field(default=None, max_length=85)
    cust_email: Optional[EmailStr] = None
    cust_social_provider: Optional[str] = Field(default=None, pattern="^(google|facebook)$")
    cust_cont_no: Optional[str] = Field(default=None, max_length=20)

    model_config = ConfigDict(from_attributes=True)


class Customer(CustomerBase):
    """
    Used for returning data from the database.
    Includes the auto-generated primary key UUID and timestamp.
    """
    cust_cd: datetime