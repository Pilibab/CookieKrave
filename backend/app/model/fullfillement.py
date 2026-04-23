from pydantic import BaseModel, ConfigDict, Field
from typing import Optional
from datetime import datetime

# ==========================================
# 1. FULFILLMENT MODELS
# ==========================================
class FulfillmentBase(BaseModel):
    # Field(pattern=...) ensures the API outright rejects any typo like "deliver" or "pickup"
    FULFILLMENT_TYPE: str = Field(pattern="^(Delivery|Pick_Up)$")

class FulfillmentCreate(FulfillmentBase):
    """Data expected from the frontend when making a new order."""
    pass

class Fulfillment(FulfillmentBase):
    """Data returned from the database."""
    FULFILLMENT_ID: int 
    
    model_config = ConfigDict(from_attributes=True)


# ==========================================
# 2. DELIVERY MODELS
# ==========================================
class DeliveryBase(BaseModel):
    # RIDER_ID is required (non-null)
    RIDER_ID: int
    ADDRESS: str = Field(max_length=255)
    
    # These are NULL in your SQL, so we use Optional[] and default=None
    CONTACT_NAME: Optional[str] = Field(default=None, max_length=100)
    CONTACT_NUMBER: Optional[str] = Field(default=None, max_length=20)
    NOTE: Optional[str] = Field(default=None, max_length=500)
    FLOOR_UNIT_NUM: Optional[str] = Field(default=None, max_length=50)

class DeliveryCreate(DeliveryBase):
    """Data expected from frontend."""
    pass

class Delivery(DeliveryBase):
    """Data returned from database."""
    FULFILLMENT_ID: int # This acts as the PK and the FK!
    
    model_config = ConfigDict(from_attributes=True)


# ==========================================
# 3. PICK UP MODELS
# ==========================================
class PickUpBase(BaseModel):
    # Both fields are nullable in your SQL
    PREFERRED_TIME: Optional[datetime] = None
    PICK_UP_LOCATION: Optional[str] = Field(default=None, max_length=255)

class PickUpCreate(PickUpBase):
    """Data expected from frontend."""
    pass

class PickUp(PickUpBase):
    """Data returned from database."""
    FULFILLMENT_ID: int
    
    model_config = ConfigDict(from_attributes=True)