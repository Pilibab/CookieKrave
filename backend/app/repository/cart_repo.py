from typing import List, cast, Any, Dict

from repository.base_repo import BaseRepository
from supabase.client import Client
from model.cart import Cart


class CartRepository(BaseRepository[Cart]):

    def __init__(self, supabase: Client):
        # Pass the actual table name and the model class to the parent
        super().__init__(supabase, "CART", Cart, "CUST_ID")

    def get_items_by_order(self, order_id: str | int) -> List[Cart]:
        # We don't use self.get_by_id because that only returns ONE record.
        # We use a custom filter to get ALL items for this order.
        response = self.table.select("*").eq("ORD_ID", order_id).execute()
        data: List[Dict[str, Any]] = cast(List[Dict[str, Any]], response.data)

        # This ensures we always return a list, even if empty, 
        # which satisfies the List[Cart] type hint.
        return [self.model_class(**item) for item in data]