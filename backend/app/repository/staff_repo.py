from supabase.client import Client
from app.model.staff import Staff, StaffCreate
from app.repository.base_repo import BaseRepository


class StaffRepository(BaseRepository[Staff, StaffCreate]):
    def __init__(self, supabase: Client):
        super().__init__(
            supabase=supabase,
            table_name="STAFF",
            model_class=Staff,
            pk_field="STAFF_ID"
        )

    # Get staff by email
    def get_by_email(self, email: str) -> Staff | None:
        """Retrieve a staff member by email"""
        result = self.get_where("STAFF_EMAIL", email)
        return result[0] if result else None

    # Get all staff with a specific role
    def get_by_role(self, role: str) -> list[Staff]:
        """Retrieve all staff members with a specific role"""
        return self.get_where("ROLE", role)
