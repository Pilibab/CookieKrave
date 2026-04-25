from typing import List, cast, Any, Dict

from repository.base_repo import BaseRepository
from supabase.client import Client
from model.fullfillement import Fulfillment, FulfillmentCreate
from model.fullfillement import Delivery, DeliveryCreate
from model.fullfillement import PickUp, PickUpCreate

class FulfillmentRepository(BaseRepository[Fulfillment, FulfillmentCreate]):
    def __init__(self, supabase: Client):
        super().__init__(supabase, "FULFILLMENT", Fulfillment, "FULFILLMENT_ID")

class DeliveryRepository(BaseRepository[Delivery, DeliveryCreate]):
    def __init__(self, supabase: Client):
        # NOTE: Using "DELIEVERY" to match your SQL schema exactly
        super().__init__(supabase, "DELIEVERY", Delivery, "FULFILLMENT_ID")

    def get_deliveries_by_rider(self, RIDER_ID: int) -> List[Delivery]:
        """Finds all delivery tasks assigned to a specific rider."""
        response = self.table.select("*").eq("RIDER_ID", RIDER_ID).execute()
        data = cast(List[Dict[str, Any]], response.data)
        return [self.model_class(**item) for item in data]

class PickUpRepository(BaseRepository[PickUp, PickUpCreate]):
    def __init__(self, supabase: Client):
        super().__init__(supabase, "PICK_UP", PickUp, "FULFILLMENT_ID")