from app.repository.base_repo import BaseRepository
from supabase.client import Client
from app.model.inventory import Inventory, InventoryCreate, InventoryUpdate
# from postgrest.types import CountMethod

class InventoryRepository(BaseRepository[Inventory, InventoryCreate, InventoryUpdate]):
    def __init__(self, supabase: Client):
        # Pass the actual table name and the model class to the parent
        super().__init__(supabase, "inventory", Inventory, "inv_id")

    def adjust_stock(self, inv_id: int, amount: float):
        """
        Increments or decrements stock. 
        Use a positive amount for restocking, negative for usage.
        """
        # Note: Using .rpc() is better for atomic math in Supabase/Postgres
        # but a simple update works if concurrency is low.
        current = self.get_by_id(inv_id)
        if current:
            new_stock = float(current.inv_stock) + amount
            return self.table.update({"inv_stock": new_stock}).eq("inv_id", inv_id).execute()
        
    # todo: maybe a get low stock method?