from typing import Any, cast, Generic, TypeVar
from pydantic import BaseModel
from supabase.client import Client


# allows base repo polymorphism 
# bounding allows data model_dump in line 32, 36 without bound data is treated as an object which 
# doesnt have model_dump method 
T = TypeVar("T", bound=BaseModel)


class BaseRepository(Generic[T]):
    # maybe pass the table itself to shorten this instanciation 
    def __init__(self, supabase: Client ,table_name: str, model_class: type[T]):
        self.table = supabase.table(table_name)
        self.model_class = model_class

    # get all row for a specific table 
    def get_all(self):
        return self.table.select("*").execute().data

    # It uses the Primary Key (the ID) to grab one specific record.
    def get_by_id(self, id: str):
        data = self.table.select("*").eq("id", id).execute().data

        if (data != []): 
            # !Argument expression after ** must be a mapping with a "str" key type
            # !from: return self.model_class(**data[0])
            # the problem is that we cant unpack a dictionary if the key to a field is not str
            # solution: ensure that data is dict[str, any] before unpacking 
            return self.model_class(**cast(dict[str, Any], data[0]))

    # It takes a Pydantic object, strips it down into a raw Dictionary (via model_dump), 
    # and pushes it into a new row in the database.
    def create(self, data: T):
        clean_data = data.model_dump()
        return self.table.insert(clean_data).execute().data

    # It finds an existing row and swaps out the old values 
    # for new ones provided in your Model.
    def update(self, id: str, data: T):
        clean_data = data.model_dump()
        return self.table.update(clean_data).eq("id", id).execute().data

    # It instructs the database to permanently erase a 
    # specific row based on its ID.
    def delete(self, id: str):
        return self.table.delete().eq("id", id).execute().data