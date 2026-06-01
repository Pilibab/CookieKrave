from app.repository.base_repo import BaseRepository
from supabase.client import Client
from app.model.order import Order, OrderCreate

from typing import List, cast, Any, Dict
from uuid import UUID
from datetime import date

class OrderRepository(BaseRepository[Order, OrderCreate]):
    def __init__(self, supabase: Client):
        # Pass the actual table name and the model class to the parent
        super().__init__(supabase, "orders", Order, "ord_id")

    def get_orders_by_customer(self, cust_id: UUID) -> List[Order]:
        """Fetches all orders made by a specific customer."""
        response = self.table.select("*").eq("cust_id", cust_id).execute()
        data = cast(List[Dict[str, Any]], response.data)
        return [self.model_class(**item) for item in data]
    
    def get_orders_between(self, week_start: date, week_end: date) -> List[Order]:
        """Fetches all orders within a date range (inclusive)."""
        response = (
            self.table
            .select("*")
            .gte("ord_time", week_start.isoformat())
            .lte("ord_time", week_end.isoformat())
            .execute()
        )
        data = cast(List[Dict[str, Any]], response.data)
        return [self.model_class(**item) for item in data]