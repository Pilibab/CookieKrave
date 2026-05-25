from typing import List

from app.repository.base_repo import BaseRepository
from supabase.client import Client
from app.model.cart import Cart, CartCreate


class CartRepository(BaseRepository[Cart, CartCreate]):

    def __init__(self, supabase: Client):
        # Pass the actual table name and the model class to the parent
        super().__init__(supabase, "cart", Cart, "cust_id")

    def get_items_by_order(self, order_id: str | int) -> List[Cart]:
        # We don't use self.get_by_id because that only returns ONE record.
        # We use a custom filter to get ALL items for this order.
        
        # same logic, for readability 
        return self.get_where("ord_id", order_id)
    
    def create_order_line(self, order_id: str | int, items: list[dict[str, int]]):
        """
            create order_line / cart from arr of items, quantity and order id
            args:
            -   order_id    : well order id 
            -   items       : items looks like: [{"prod_id": 101, "cart_quan": 2}, ...]
        """
        for item in items:
            item_instance = CartCreate(
                ord_id=int(order_id),       # i think its better if id is of str
                prod_id=item["prod_id"],
                cart_quan=item["cart_quan"]
            )
            self.create(item_instance)