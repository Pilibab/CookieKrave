from typing import List, cast, Any, Dict

from repository.base_repo import BaseRepository
from supabase.client import Client
from model.bom import Bom

class BOMRepository(BaseRepository[Bom]):
    def __init__(self, supabase: Client):
        super().__init__(supabase, "BOM", Bom, "BOM_ID")

    def get_recipe_for_product(self, PROD_ID: int) -> List[Bom]:
        """Fetches all ingredients and quantities required for a specific product."""
        response = self.table.select("*").eq("PROD_ID", PROD_ID).execute()
        data = cast(List[Dict[str, Any]], response.data)
        return [self.model_class(**item) for item in data]
        
    def get_products_using_ingredient(self, INV_ID: int) -> List[Bom]:
        """Finds all products that use a specific inventory item."""
        response = self.table.select("*").eq("INV_ID", INV_ID).execute()
        data = cast(List[Dict[str, Any]], response.data)

        return [self.model_class(**item) for item in data]
    