from pydantic import BaseModel, ConfigDict, Field
from typing import Optional
from datetime import datetime

# ==========================================
# 1. FULFILLMENT MODELS
# ==========================================
class FulfillmentBase(BaseModel):
    # Field(pattern=...) ensures the API outright rejects any typo like "deliver" or "pickup"
    fulfillment_type: str = Field(pattern="^(Delivery|Pick_Up)$")

class FulfillmentCreate(FulfillmentBase):
    """Data expected from the frontend when making a new order."""
    pass

class Fulfillment(FulfillmentBase):
    """Data returned from the database."""
    fulfillment_id: int 
    
    model_config = ConfigDict(from_attributes=True)


# ==========================================
# 2. DELIVERY MODELS
# ==========================================
class DeliveryBase(BaseModel):
    # rider_id is required (non-null)
    rider_id: int
    address: str = Field(max_length=255)
    
    # These are NULL in your SQL, so we use Optional[] and default=None
    contact_name: Optional[str] = Field(default=None, max_length=100)
    contact_number: Optional[str] = Field(default=None, max_length=20)
    note: Optional[str] = Field(default=None, max_length=500)
    floor_unit_num: Optional[str] = Field(default=None, max_length=50)

class DeliveryCreate(DeliveryBase):
    """Data expected from frontend."""
    pass

class Delivery(DeliveryBase):
    """Data returned from database."""
    fulfillment_id: int # This acts as the PK and the FK!
    
    model_config = ConfigDict(from_attributes=True)


# ==========================================
# 3. PICK UP MODELS
# ==========================================
class PickUpBase(BaseModel):
    # Both fields are nullable in your SQL
    preferred_time: Optional[datetime] = None
    pick_up_location: Optional[str] = Field(default=None, max_length=255)

class PickUpCreate(PickUpBase):
    """Data expected from frontend."""
    pass

class PickUp(PickUpBase):
    """Data returned from database."""
    fulfillment_id: int
    
    model_config = ConfigDict(from_attributes=True)

    # ==========================================
# 1. FULFILLMENT UPDATE
# ==========================================
class FulfillmentUpdate(BaseModel):
    """
    Used to update the root fulfillment metadata.
    """
    # Keep the pattern guard so the frontend can't accidentally send a typo
    fulfillment_type: Optional[str] = Field(default=None, pattern="^(Delivery|Pick_Up)$")


# ==========================================
# 2. DELIVERY UPDATE
# ==========================================
class DeliveryUpdate(BaseModel):
    """
    Used for partial updates to a delivery profile (e.g., assigning a new rider, updating notes).
    """
    rider_id: Optional[int] = None
    address: Optional[str] = Field(default=None, max_length=255)
    contact_name: Optional[str] = Field(default=None, max_length=100)
    contact_number: Optional[str] = Field(default=None, max_length=20)
    note: Optional[str] = Field(default=None, max_length=500)
    floor_unit_num: Optional[str] = Field(default=None, max_length=50)


# ==========================================
# 3. PICK UP UPDATE
# ==========================================
class PickUpUpdate(BaseModel):
    """
    Used for partial updates to a customer pickup schedule or location.
    """
    preferred_time: Optional[datetime] = None
    pick_up_location: Optional[str] = Field(default=None, max_length=255)