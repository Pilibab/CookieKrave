from app.repository.base_repo import BaseRepository
from supabase.client import Client
from app.model.order import Order, OrderCreate

from typing import List, cast, Any, Dict

class OrderRepository(BaseRepository[Order, OrderCreate]):
    def __init__(self, supabase: Client):
        # Pass the actual table name and the model class to the parent
        super().__init__(supabase, "orders", Order, "ord_id")

    def get_orders_by_customer(self, cust_id: int) -> List[Order]:
        """Fetches all orders made by a specific customer."""
        response = self.table.select("*").eq("cust_id", cust_id).execute()
        data = cast(List[Dict[str, Any]], response.data)
        return [self.model_class(**item) for item in data]