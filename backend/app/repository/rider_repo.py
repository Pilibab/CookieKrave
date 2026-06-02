from app.repository.base_repo import BaseRepository
from supabase.client import Client
from app.model.rider import Rider, RiderCreate, RiderUpdate

class RiderRepository(BaseRepository[Rider, RiderCreate, RiderUpdate]):
    def __init__(self, supabase: Client):
        super().__init__(supabase, "rider", Rider, "rider_id")

    # def update_location(self, rider_id: int, new_location: str):
    #     """Quick method to update a rider's real-time location."""
    #     return self.table.update({"current_location": new_location}).eq("rider_id", rider_id).execute().data
