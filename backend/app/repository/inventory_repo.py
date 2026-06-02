from app.repository.base_repo import BaseRepository
from supabase.client import Client
from app.model.inventory import Inventory, InventoryCreate, InventoryUpdate
# from postgrest.types import CountMethod

from decimal import Decimal
from typing import Any, Dict

class InventoryRepository(BaseRepository[Inventory, InventoryCreate, InventoryUpdate]):
    def __init__(self, supabase: Client):
        # Pass the actual table name and the model class to the parent
        super().__init__(supabase, "inventory", Inventory, "inv_id")

    def adjust_stock(self, inv_id: int, amount: Decimal):
        """
        Increments or decrements stock. 
        Use a positive amount for restocking, negative for usage.
        """
        current = self.get_by_id(inv_id)
        if current:
            # 1. FIXED: Keep math completely native. Decimal + Decimal = Decimal.
            # Adding the type hint ': Decimal' resolves the 'Unknown Variable Type' warning.
            new_stock: Decimal = current.inv_stock + amount
            
            # 2. FIXED: PostgREST/Supabase JSON encoders don't natively serialize 
            # Python Decimal objects. We convert it to a float ONLY here at the 
            # database payload boundary. Since the arithmetic is already finished, 
            # no rounding precision errors will occur.
            payload: Dict[str, Any] = {"inv_stock": float(new_stock)}
            
            return self.table.update(payload).eq("inv_id", inv_id).execute()