from repository.base_repo import BaseRepository
from supabase.client import Client
from model.customer import Customer
from postgrest.types import CountMethod

class CustomerRepository(BaseRepository[Customer]):
    def __init__(self, supabase: Client):
        # Pass the actual table name and the model class to the parent
        super().__init__(supabase, "CUSTOMERS", Customer)

    def get_by_email(self, email: str): 
        self.table.select("*").eq("email", email).execute()

    def get_by_social_id(self, provider: str, social_id: str):
        return self.table.select("*"). \
                eq("social_provider", provider).\
                eq("social_id", social_id).execute()
    
    def get_by_phone(self, phone_number: str):
        self.table.select("*").eq("contact_number", phone_number).execute()

    # validation 
    def is_email_taken(self, email: str) -> bool:
        result = self.table.select("*", count=CountMethod.exact, head=True).\
                            eq("email", email).execute()

        return self.validate_existence(result)
        

    def is_phone_registered(self, phone_number: str):
        result = self.table.select("*", count=CountMethod.exact, head=True).\
                            eq("contact_number", phone_number).execute()
        
        return self.validate_existence(result)

        