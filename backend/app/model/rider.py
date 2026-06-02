from pydantic import BaseModel, ConfigDict, Field
from typing import Optional

class RiderBase(BaseModel):
    """
    Base data fields shared across reading, creating, and updating riders.
    Matches your character varying length constraints exactly.
    """
    rider_name: str = Field(min_length=5, max_length=100)
    rider_contact_num: str = Field(min_length=5, max_length=20) 

    model_config = ConfigDict(from_attributes=True)


class RiderCreate(RiderBase):
    """
    Used when registering a rider.
    The rider_id is a string fetched directly from your 3rd-party delivery provider.
    """
    rider_id: str = Field(min_length=1, max_length=64)


class RiderUpdate(BaseModel):
    """
    Used for partial profile updates.
    (Note: rider_id is omitted here because you won't change an external system's ID).
    """
    rider_name: Optional[str] = Field(default=None, min_length=5, max_length=100)
    rider_contact_num: Optional[str] = Field(default=None, min_length=5, max_length=20)

    model_config = ConfigDict(from_attributes=True)


class Rider(RiderBase): 
    """
    Used for returning data back from Supabase/PostgreSQL.
    Includes the string-based primary key ID.
    """
    rider_id: str