from datetime import date
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field

class ProductBase(BaseModel):
    """
    Base fields shared for reading and creating products.
    Matches the exact constraints of the public.products database columns.
    """
    prod_name: str = Field(min_length=5, max_length=64)
    prod_desc: str = Field(min_length=5, max_length=255)
    
    # ge=0 enforces the CHECK constraint (prod_price >= 0)
    prod_price: float = Field(ge=0.0) 
    prod_available: bool = True
    
    # ADDED: Aligns with 'prod_sl date not null'
    prod_sl: date 
    
    # ADDED: Aligns with 'prod_image_url character varying(512)' and its fallback default
    prod_image_url: Optional[str] = Field(
        default="https://ghhowjijwfgffcbjlsxl.supabase.co/storage/v1/object/public/product_img/default_no_img.png",
        max_length=512
    )

    # Configures Pydantic to cleanly convert SQLAlchemy/SQL objects into dictionaries/JSON
    model_config = ConfigDict(from_attributes=True)


class ProductCreate(ProductBase):
    """
    Used when receiving data from the Frontend to create a new record.
    Inherits all base fields. The database generates the 'prod_id' automatically.
    """
    pass


class Product(ProductBase): 
    """
    Used for reading data from the database. 
    Includes the auto-generated database primary key ID.
    """
    prod_id: int

class ProductUpdate(BaseModel):
    """
    Used when receiving data from the Frontend to update an existing record.
    All fields are completely optional to allow for flexible partial updates.
    """
    # Notice we set default=None, but keep the core validation constraints!
    prod_name: Optional[str] = Field(default=None, min_length=5, max_length=64)
    prod_desc: Optional[str] = Field(default=None, min_length=5, max_length=255)
    prod_price: Optional[float] = Field(default=None, ge=0.0) 
    prod_available: Optional[bool] = None
    prod_sl: Optional[date] = None 
    prod_image_url: Optional[str] = Field(default=None, max_length=512)

    model_config = ConfigDict(from_attributes=True)