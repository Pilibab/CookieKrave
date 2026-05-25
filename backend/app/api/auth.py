from fastapi import APIRouter, Depends
from app.api.deps import get_current_user
from typing import Any

from app.db.supabase_client import supabase 
from typing import Any
# Define the router instead of importing app
router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    # dependencies=[Depends(get_current_user)]
)

@router.get("/me", summary="Validate token and return current user profile")
def get_authenticated_user(current_user: dict[str, Any] = Depends(get_current_user)) -> dict[str, Any]:
    """
    determins if the user is an admin/staff member.
    """
    user_id = current_user.get("sub") # Supabase stores the user ID in the 'sub' claim
    
    # Check if this user exists in your staff/admin table
    # Adjust this query based on how your 00_staff.sql is structured!
    response = supabase.table("staff").select("id").eq("auth_id", user_id).execute()
    
    # If a record comes back, they are staff. Otherwise, standard customer.
    is_admin = len(response.data) > 0
    
    # Attach it to the payload for the Next.js frontend to read
    return {
        **current_user,
        "is_admin": is_admin,
        "role": "admin" if is_admin else "customer"
    }