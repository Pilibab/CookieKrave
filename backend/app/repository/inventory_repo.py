from repository.base_repo import BaseRepository
from supabase.client import Client
from model.inventory import Inventory, InventoryCreate
# from postgrest.types import CountMethod

class InventoryRepository(BaseRepository[Inventory, InventoryCreate]):
    def __init__(self, supabase: Client):
        # Pass the actual table name and the model class to the parent
        super().__init__(supabase, "INVENTORY", Inventory, "INV_ID")

    def adjust_stock(self, INV_ID: int, amount: float):
        """
        Increments or decrements stock. 
        Use a positive amount for restocking, negative for usage.
        """
        # Note: Using .rpc() is better for atomic math in Supabase/Postgres
        # but a simple update works if concurrency is low.
        current = self.get_by_id(str(INV_ID))
        if current:
            new_stock = float(current.INV_STOCK) + amount
            return self.table.update({"INV_STOCK": new_stock}).eq("INV_ID", INV_ID).execute()
        
    # todo: maybe a get low stock method?