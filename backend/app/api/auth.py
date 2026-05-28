from fastapi import APIRouter, Depends, HTTPException
from typing import Any
from nameparser import HumanName

from app.repository.customer_repo import CustomerRepository
from app.model.customer import CustomerCreate
from app.api.deps import get_current_user
from app.db.supabase_client import supabase_admin 
# Define the router instead of importing app
router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    # dependencies=[Depends(get_current_user)]
)

@router.get("/me", summary="Validate token and return current user profile")
def sync_user_profile(current_user: dict[str, Any] = Depends(get_current_user)) -> dict[str, Any]:
    """
    determins if the user is an admin/staff member.
    """
    # initialize repo
    print(current_user)
    cust_repo = CustomerRepository(supabase_admin)

    user_id = current_user.get("sub") 
    email = current_user.get("email")

    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token claims: missing 'sub'.")
    
    if not email:
        raise HTTPException(status_code=401, detail="Missing email.")
    
    provider = current_user.get("app_metadata", {}).get("provider")
    full_name = HumanName(current_user.get("user_metadata", {}).get("full_name"))
    first_name = full_name.first
    middle_name = full_name.middle
    last_name = full_name.last

    # Initialize fallback flags safely at the top level scope
    is_admin = False
    
    try: 
        #! use repo for this 
        staff_res = supabase_admin.table("staff").select("id").eq("staff_id", user_id).execute()

        # checks if the token bearer has admin role
        if len(staff_res.data) > 0:
            return {"is_admin": True, "role": "admin", "email": email}

        if cust_repo.is_social_user_registered(user_id):
            new_customer = CustomerCreate(
                cust_firstname=first_name,
                cust_lastname=last_name,
                cust_middlename=middle_name if middle_name else "",
                cust_email=email,
                cust_cont_no=current_user.get("phone") or "Not Provided",
                cust_social_provider=provider,
            )

            cust_repo.create(new_customer)
    except Exception as e:
        print(f"Database error verifying staff status: {str(e)}")
        # Fallback to False to protect app stability if DB connections stutter
        is_admin = False
    # Attach it to the payload for the Next.js frontend to read
    return {
        **current_user,
        "is_admin": is_admin,
        "role": "admin" if is_admin else "customer"
    }