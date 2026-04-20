from repository.base_repo import BaseRepository
from supabase.client import Client
from model.customer import Customer
from postgrest.types import CountMethod

class CustomerRepository(BaseRepository[Customer]):
    def __init__(self, supabase: Client):
        # Pass the actual table name and the model class to the parent
        super().__init__(supabase, "CUSTOMERS", Customer, "CUST_ID")

    def get_by_email(self, CUST_EMAIL: str): 
        self.table.select("*").eq("CUST_EMAIL", CUST_EMAIL).execute()

    def get_by_social_id(self, provider: str, CUST_SOCIALID: str):
        return self.table.select("*"). \
                eq("CUST_SOCIAL_PROVIDER", provider).\
                eq("CUST_SOCIALID", CUST_SOCIALID).execute()
    
    def get_by_phone(self, phone_number: str):
        self.table.select("*").eq("CUST_CONT_NO", phone_number).execute()

    # validation 
    def is_email_taken(self, CUST_EMAIL: str) -> bool:
        result = self.table.select("*", count=CountMethod.exact, head=True).\
                            eq("CUST_EMAIL", CUST_EMAIL).execute()

        return self.validate_existence(result)
        

    def is_phone_registered(self, phone_number: str):
        result = self.table.select("*", count=CountMethod.exact, head=True).\
                            eq("CUST_CONT_NO", phone_number).execute()
        
        return self.validate_existence(result)

        