from pydantic import BaseModel, ConfigDict, Field

class ProductBase(BaseModel):
    """
        used for reading data from the data base
    """
    PROD_ID: int 

    # allows pydantic to work with sql, pydantic expects a dict but sql returns an object 
    # setting it to true says that if bracket notation dict["key"] does not work try obj.method
    model_config = ConfigDict(from_attributes=True)

class Product(ProductBase): 
    PROD_NAME: str = Field(min_length=5, max_length=64)
    PROD_DESC: str = Field(min_length=5, max_length=255)
    PROD_PRICE: float                                                # set the float to 7 width 2 decimal place
    PROD_AVAILABLE: bool = True


class ProductCreate(BaseModel):
    """
        Used when receiving data from the Frontend (ID isn't created yet) 
    """
    pass