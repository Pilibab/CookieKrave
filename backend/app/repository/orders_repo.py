from repository.base_repo import BaseRepository
from supabase.client import Client
from model.order import Order

class OrderRepository(BaseRepository[Order]):
    def __init__(self, supabase: Client):
        # Pass the actual table name and the model class to the parent
        super().__init__(supabase, "ORDERS", Order, "ORD_ID")

    # def get_total_cost(self, order_id)
    #     pass