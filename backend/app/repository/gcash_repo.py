# app/repository/gcash_repo.py
from supabase import Client
from app.repository.base_repo import BaseRepository
from app.model.gcash import GCashPayment, GCashPaymentCreate

class GCashRepository(BaseRepository[GCashPayment, GCashPaymentCreate]):
    def __init__(self, supabase: Client):
        super().__init__(supabase, "gcash_payments", GCashPayment, "ord_id")

    def get_by_order(self, ord_id: int) -> GCashPayment | None:
        return self.get_by_id(ord_id)  # ord_id IS the PK, so base method handles it