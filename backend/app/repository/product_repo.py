from app.repository.base_repo import BaseRepository
from supabase.client import Client
from app.model.products import Product, ProductCreate, ProductUpdate
# from postgrest.types import CountMethod

class ProductRepository(BaseRepository[Product, ProductCreate, ProductUpdate]):
    def __init__(self, supabase: Client):
        # Pass the actual table name and the model class to the parent
        super().__init__(supabase, "products", Product, "prod_id")
    
    def get_available_product(self):
        """return all product marked as available"""
        return self.table.select("*").eq("prod_available", True).execute()

    def search_product_by_name(self, query: str):
        """return product with matching name, case insensitive""" 
        # f"{search_term}%": Matches anything starting with your term.
        #     Search: "App" -> Matches: "Apple", "Appricot".
        # f"%{search_term}": Matches anything ending with your term.
        #     Search: "berry" -> Matches: "Strawberry", "Blueberry".
        # f"%{search_term}%": Matches anything that contains your term anywhere.
        #     Search: "ice" -> Matches: "Ice cream", "Rice", "Priceless".
        
        return self.table.select("*").ilike("prod_name", f"{query}%").execute()