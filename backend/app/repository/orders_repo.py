from repository.base_repo import BaseRepository
from supabase.client import Client
from model.order import Order

from typing import List, cast, Any, Dict

class OrderRepository(BaseRepository[Order]):
    def __init__(self, supabase: Client):
        # Pass the actual table name and the model class to the parent
        super().__init__(supabase, "ORDERS", Order, "ORD_ID")

    def get_orders_by_customer(self, CUST_ID: int) -> List[Order]:
        """Fetches all orders made by a specific customer."""
        response = self.table.select("*").eq("CUST_ID", CUST_ID).execute()
        data = cast(List[Dict[str, Any]], response.data)
        return [self.model_class(**item) for item in data]