from repository.base_repo import BaseRepository
from supabase.client import Client
from model.rider import Rider

class RiderRepository(BaseRepository[Rider]):
    def __init__(self, supabase: Client):
        super().__init__(supabase, "RIDER", Rider, "RIDER_ID")

    def update_location(self, RIDER_ID: int, new_location: str):
        """Quick method to update a rider's real-time location."""
        return self.table.update({"CURRENT_LOCATION": new_location}).eq("RIDER_ID", RIDER_ID).execute().data
