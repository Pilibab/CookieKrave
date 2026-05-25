from pydantic import BaseModel, ConfigDict, Field, EmailStr
from typing import Optional
from uuid import UUID

class StaffBase(BaseModel):
    """
        Used for reading data from the database
    """
    STAFF_NAME: str = Field(min_length=1, max_length=64)
    STAFF_EMAIL: EmailStr
    ROLE: str = Field(default='admin', pattern="^(admin|manager|baker)$")

    # This allows Pydantic to work with SQLAlchemy/SQLModel objects
    model_config = ConfigDict(from_attributes=True)


class Staff(StaffBase):
    STAFF_ID: UUID


class StaffCreate(BaseModel):
    """Used when receiving data from the Frontend (ID isn't created yet)"""
    STAFF_NAME: str = Field(min_length=1, max_length=64)
    STAFF_EMAIL: EmailStr
    ROLE: Optional[str] = Field(default='admin', pattern="^(admin|manager|baker)$")

    model_config = ConfigDict(from_attributes=True)
