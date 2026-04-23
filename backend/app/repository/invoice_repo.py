from typing import Optional, cast, Any

from repository.base_repo import BaseRepository
from supabase.client import Client
from model.invoice import Invoice


class InvoiceRepository(BaseRepository[Invoice]): 
    def __init__(self, supabase: Client):
        super().__init__(supabase, "INVOICES", Invoice, "INVOICE_ID")

    def get_invoice_by_order(self, ORD_ID: int) -> Optional[Invoice]:
        """Fetches the specific invoice tied to an order."""
        data = self.table.select("*").eq("ORD_ID", ORD_ID).execute().data
        if data != []:
            return self.model_class(**cast(dict[str, Any], data[0]))
        return None