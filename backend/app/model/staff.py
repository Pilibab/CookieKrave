from pydantic import BaseModel, ConfigDict, Field, EmailStr
from typing import Optional
from uuid import UUID

class StaffBase(BaseModel):
    """
        Used for reading data from the database
    """
    staff_name: str = Field(min_length=1, max_length=64)
    staff_email: EmailStr
    role: str = Field(default='admin', pattern="^(admin|manager|baker)$")

    # This allows Pydantic to work with SQLAlchemy/SQLModel objects
    model_config = ConfigDict(from_attributes=True)


class Staff(StaffBase):
    staff_id: UUID


class StaffCreate(BaseModel):
    """Used when receiving data from the Frontend (ID isn't created yet)"""
    staff_name: str = Field(min_length=1, max_length=64)
    staff_email: EmailStr
    role: Optional[str] = Field(default='admin', pattern="^(admin|manager|baker)$")

    model_config = ConfigDict(from_attributes=True)
