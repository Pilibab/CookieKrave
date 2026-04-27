from typing import Any, cast, Generic, TypeVar, Optional
from pydantic import BaseModel
from supabase.client import Client
from postgrest import APIResponse

# allows base repo polymorphism 
# bounding allows data model_dump in line 32, 36 without bound data is treated as an object which 
# doesnt have model_dump method 
T = TypeVar("T", bound=BaseModel)       # read model
C = TypeVar("C", bound=BaseModel)       # create model 


class BaseRepository(Generic[T, C]):
    # maybe pass the table itself to shorten this instanciation 
    def __init__(
            self, 
            supabase: Client,
            table_name: str, 
            model_class: type[T],
            pk_field: str = "id"    # for dynamic id in each database
            ):
        self.table = supabase.table(table_name)
        self.model_class = model_class
        self.pk_field = pk_field

    # get all row for a specific table 
    def get_all(self):
        """retrieve the full table"""
        return self.table.select("*").execute().data

    # It uses the Primary Key (the ID) to grab one specific record.
    def get_by_id(self, id: str | int) -> Optional[T]:
        """get an instance from a table (that is not an associative entity), using only one id"""
        data = self.table.select("*").eq(self.pk_field , id).execute().data

        if (data != []): 
            # !Argument expression after ** must be a mapping with a "str" key type
            # !from: return self.model_class(**data[0])
            # the problem is that we cant unpack a dictionary if the key to a field is not str
            # solution: ensure that data is dict[str, any] before unpacking 
            return self.model_class(**cast(dict[str, Any], data[0]))

    # Retrieve all instances matching a specific field and value
    def get_where(self, field_name: str, value: Any) -> list[T]:
        """
        Used for associative entities (e.g., getting all items in a Cart).
        Returns a list of Pydantic objects.
        """
        result = self.table.select("*").eq(field_name, value).execute()
        
        # result.data is a list of dictionaries: list[dict[str, Any]]
        # We map each dictionary in the list to your model_class
        return [
            self.model_class(**cast(dict[str, Any], row)) 
            for row in result.data
        ]

    # It takes a Pydantic object, strips it down into a raw Dictionary (via model_dump), 
    # and pushes it into a new row in the database.
    def create(self, data: C):
        clean_data = data.model_dump()
        result = self.table.insert(clean_data).execute().data

        return self.model_class(**cast(dict[str, Any], result[0]))

    # It finds an existing row and swaps out the old values 
    # for new ones provided in your Model.
    def update(self, id: str, data: T):
        clean_data = data.model_dump()
        return self.table.update(clean_data).eq(self.pk_field , id).execute().data

    # It instructs the database to permanently erase a 
    # specific row based on its ID.
    def delete(self, id: str):
        return self.table.delete().eq(self.pk_field , id).execute().data
    
    #existence checker
    # helper probably move this to its own file 
    def validate_existence(self, result: APIResponse) -> bool:
        """
        Checks the API result for a valid count. 
        Fails loudly if the count is missing (connection/API error).
        """
        # Check for connection/query errors first
        # worried that since None will occur if the user lost its connection, if 
        # none returns false it may allow the user to create an account or whatever 
        # regardless if 2 customer has the same gmail upon reconnecting 
        if result.count is None:
            raise RuntimeError("Database failed to return a count. Check connection.")
        
        return result.count > 0 