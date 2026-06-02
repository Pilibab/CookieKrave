from typing import List, cast, Any, Dict

from app.repository.base_repo import BaseRepository
from supabase.client import Client
from app.model.bom import Bom, BomCreate, BomUpdate

class BOMRepository(BaseRepository[Bom, BomCreate, BomUpdate]):
    def __init__(self, supabase: Client):
        super().__init__(supabase, "bom", Bom, "bom_id")

    def get_stock(self, prod_id: int) -> List[Bom]:
        """Fetches all ingredients and quantities required for a specific product."""
        return self.get_where("prod_id", prod_id)
        
    def get_products_using_ingredient(self, inv_id: int) -> List[Bom]:
        """Finds all products that use a specific inventory item."""
        response = self.table.select("*").eq("inv_id", inv_id).execute()
        data = cast(List[Dict[str, Any]], response.data)

        return [self.model_class(**item) for item in data]
    