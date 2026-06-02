from typing import List, cast, Any, Dict

from app.repository.base_repo import BaseRepository
from supabase.client import Client
from app.model.fullfillement import Fulfillment, FulfillmentCreate, FulfillmentUpdate
from app.model.fullfillement import Delivery, DeliveryCreate, DeliveryUpdate
from app.model.fullfillement import PickUp, PickUpCreate, PickUpUpdate

class FulfillmentRepository(BaseRepository[Fulfillment, FulfillmentCreate, FulfillmentUpdate]):
    def __init__(self, supabase: Client):
        super().__init__(supabase, "fulfillment", Fulfillment, "fulfillment_id")

class DeliveryRepository(BaseRepository[Delivery, DeliveryCreate,DeliveryUpdate]):
    def __init__(self, supabase: Client):
        # NOTE: Using "delivery" to match your SQL schema
        super().__init__(supabase, "delivery", Delivery, "fulfillment_id")

    def get_deliveries_by_rider(self, rider_id: int) -> List[Delivery]:
        """Finds all delivery tasks assigned to a specific rider."""
        response = self.table.select("*").eq("rider_id", rider_id).execute()
        data = cast(List[Dict[str, Any]], response.data)
        return [self.model_class(**item) for item in data]

class PickUpRepository(BaseRepository[PickUp, PickUpCreate, PickUpUpdate]):
    def __init__(self, supabase: Client):
        super().__init__(supabase, "pick_up", PickUp, "fulfillment_id")