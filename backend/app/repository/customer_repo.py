from app.repository.base_repo import BaseRepository
from supabase.client import Client
from app.model.customer import Customer, CustomerCreate
from postgrest.types import CountMethod
from uuid import UUID
class CustomerRepository(BaseRepository[Customer, CustomerCreate]):
    def __init__(self, supabase: Client):
        # Pass the actual table name and the model class to the parent
        super().__init__(supabase, "customers", Customer, "cust_id")

    def get_by_email(self, cust_email: str): 
        self.table.select("*").eq("cust_email", cust_email).execute()

    # def get_by_social_id(self, provider: str, cust_social_id: str):
    #     return self.table.select("*"). \
    #             eq("cust_social_provider", provider).\
    #             eq("cust_social_id", cust_social_id).execute()
    
    def get_by_phone(self, phone_number: str):
        self.table.select("*").eq("cust_cont_no", phone_number).execute()

    # validation 
    def is_email_taken(self, cust_email: str) -> bool:
        result = self.table.select("*", count=CountMethod.exact, head=True).\
                            eq("cust_email", cust_email).execute()

        return self.validate_existence(result)
        

    def is_phone_registered(self, phone_number: str):
        result = self.table.select("*", count=CountMethod.exact, head=True).\
                            eq("cust_cont_no", phone_number).execute()
        
        return self.validate_existence(result)

    def is_user_registered(self, cust_id: UUID) -> bool:
        """Checks if this specific Google/Facebook account has a profile yet."""
        result = self.table.select("cust_id", count=CountMethod.exact, head=True) \
            .eq("cust_id", cust_id) \
            .execute()
        return self.validate_existence(result)