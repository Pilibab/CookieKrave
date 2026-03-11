from pydantic import BaseModel, ConfigDict, Field

class ProductBase(BaseModel):
    """
        used for reading data from the data base
    """
    product_id: int 

    # allows pydantic to work with sql, pydantic expects a dict but sql returns an object 
    # setting it to true says that if bracket notation dict["key"] does not work try obj.method
    model_config = ConfigDict(from_attributes=True)

class Product(BaseModel): 
    product_name: str = Field(min_length=5, max_length=64)
    product_desc: str = Field(min_length=5, max_length=255)
    price: float                                                # set the float to 7 width 2 decimal place
    is_available: bool = True


class ProductCreate(ProductBase):
    """
        Used when receiving data from the Frontend (ID isn't created yet) 
    """
    pass