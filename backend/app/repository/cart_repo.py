from typing import List, cast, Any, Dict

from repository.base_repo import BaseRepository
from supabase.client import Client
from model.cart import Cart, CartCreate


class CartRepository(BaseRepository[Cart, CartCreate]):

    def __init__(self, supabase: Client):
        # Pass the actual table name and the model class to the parent
        super().__init__(supabase, "CART", Cart, "CUST_ID")

    def get_items_by_order(self, order_id: str | int, cust_id: str | int) -> List[Cart]:
        # We don't use self.get_by_id because that only returns ONE record.
        # We use a custom filter to get ALL items for this order.
        response = self.table.select("*")   \
            .eq("ORD_ID", order_id) \
            .eq("CUST_ID", cust_id).execute()
        
        data: List[Dict[str, Any]] = cast(List[Dict[str, Any]], response.data)

        # This ensures we always return a list, even if empty, 
        # which satisfies the List[Cart] type hint.
        return [self.model_class(**item) for item in data]
    
    def create_order_line(self, order_id: str | int, items: list[dict[str, int]]):
        """
            create order_line / cart from arr of items, quantity and order id
            args:
            -   order_id    : well order id 
            -   items       : items looks like: [{"PROD_ID": 101, "CART_QUAN": 2}, ...]
        """
        for item in items:
            item_instance = CartCreate(
                ORD_ID=int(order_id),       # i think its better if id is of str
                PROD_ID=item["PROD_ID"],
                CART_QUAN=item["CART_QUAN"]
            )
            self.create(item_instance)