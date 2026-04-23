from pydantic import BaseModel, ConfigDict, Field

class RiderBase(BaseModel):
    """
        used for reading data from the data base
    """
    RIDER_ID: int 

    # allows pydantic to work with sql, pydantic expects a dict but sql returns an object 
    # setting it to true says that if bracket notation dict["key"] does not work try obj.method
    model_config = ConfigDict(from_attributes=True)

class Rider(RiderBase): 
    RIDER_NAME: str = Field(min_length=5, max_length=100)
    RIDER_CONTACT_NUM: str = Field(min_length=5, max_length=20)                                                # set the float to 7 width 2 decimal place
    CURRENT_LOCATION: str = Field(min_length=5, max_length=255)


class RiderCreate(BaseModel):
    """
        Used when receiving data from the Frontend (ID isn't created yet) 
    """
    pass