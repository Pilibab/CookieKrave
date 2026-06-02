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

# @router.get("/me", summary="Validate token and return current user profile")
# def sync_user_profile(current_user: dict[str, Any] = Depends(get_current_user)) -> dict[str, Any]:
#     """
#     determins if the user is an admin/staff member.
#     """
#     # initialize repo
#     # print(current_user)
#     cust_repo = CustomerRepository(supabase_admin)

#     user_id = current_user.get("sub") 
#     email = current_user.get("email")
#     cust_id=current_user.get("sub")

#     if not user_id:
#         raise HTTPException(status_code=401, detail="Invalid token claims: missing 'sub'.")
    
#     if not cust_id:
#         raise HTTPException(status_code=401, detail="Missing email.")
    
#     if not email:
#         raise HTTPException(status_code=401, detail="Missing jwt identifier.")
    
#     provider = current_user.get("app_metadata", {}).get("provider")
#     full_name = HumanName(current_user.get("user_metadata", {}).get("full_name"))
#     first_name = full_name.first.title()
#     middle_name = full_name.middle.title()
#     last_name = full_name.last.title()

#     # Initialize fallback flags safely at the top level scope
#     is_admin = False
    
#     try: 
#         #! use repo for this 
#         staff_res = supabase_admin.table("staff").select("staff_id").eq("staff_id", user_id).execute()

#         # checks if the token bearer has admin role
#         if len(staff_res.data) > 0:
#             return {"is_admin": True, "role": "admin", "email": email}

#         if not cust_repo.is_user_registered(user_id):
#             new_customer = CustomerCreate(
#                 cust_id=cust_id,
#                 cust_firstname=first_name,
#                 cust_lastname=last_name,
#                 cust_middlename=middle_name if middle_name else "",
#                 cust_email=email,
#                 cust_cont_no=current_user.get("phone") or "Not Provided",
#                 cust_social_provider=provider,
#             )
#             cust_repo.create(new_customer)
#     except Exception as e:
#         print(f"[CRITICAL AUTH FAILURE] Database error during identity sync: {str(e)}")
#         # FAIL LOUDLY: Stop the login flow if the database stutters!
#         raise HTTPException(
#             status_code=500, 
#             detail="Identity synchronization engine failure. Please try again later."
#         )
#     return {
#         **current_user,
#         "is_admin": is_admin,
#         "role": "admin" if is_admin else "customer"
#     }

# ! pray that this work
@router.get("/me", summary="Validate token and return current user profile")
def sync_user_profile(current_user: dict[str, Any] = Depends(get_current_user)) -> dict[str, Any]:
    """
    Validates token claims, synchronizes customer information if unregistered,
    and returns a standardized profile matching frontend interface contract expectations.
    """
    user_id = current_user.get("sub") 
    email = current_user.get("email")

    # 1. Fixed & Cleaned Validation Check Guards
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token claims: missing 'sub' (user identifier).")
    if not email:
        raise HTTPException(status_code=401, detail="Invalid token claims: missing account 'email'.")
    
    # 2. Extract metadata parameters uniformly
    user_metadata = current_user.get("user_metadata", {})
    provider = current_user.get("app_metadata", {}).get("provider", "google")
    
    # Clean string processing for full names & fallbacks
    display_name = user_metadata.get("full_name") or user_metadata.get("name") or email.split("@")[0]
    image_url = user_metadata.get("avatar_url") or user_metadata.get("picture") or ""

    full_name = HumanName(display_name)
    first_name = full_name.first.title()
    middle_name = full_name.middle.title()
    last_name = full_name.last.title()

    cust_repo = CustomerRepository(supabase_admin)
    
    try: 
        # Check database if user belongs to staff list
        staff_res = supabase_admin.table("staff").select("staff_id").eq("staff_id", user_id).execute()

        # CASE A: User is an Administrator/Staff member
        if len(staff_res.data) > 0:
            return {
                "user": {
                    "id": user_id,
                    "email": email,
                    "name": display_name,
                    "image": image_url,
                    "role": "admin"
                }
            }

        # CASE B: User is a Customer. Handle lazy registration verification check
        if not cust_repo.is_user_registered(user_id):
            new_customer = CustomerCreate(
                cust_id=user_id,
                cust_firstname=first_name,
                cust_lastname=last_name,
                cust_middlename=middle_name if middle_name else "",
                cust_email=email,
                cust_cont_no=current_user.get("phone") or "Not Provided",
                cust_social_provider=provider,
            )
            cust_repo.create(new_customer)
            
        return {
            "user": {
                "id": user_id,
                "email": email,
                "name": display_name,
                "image": image_url,
                "role": "customer"
            }
        }

    except Exception as e:
        print(f"[CRITICAL AUTH FAILURE] Database error during identity sync: {str(e)}")
        raise HTTPException(
            status_code=500, 
            detail="Identity synchronization engine failure. Please try again later."
        )