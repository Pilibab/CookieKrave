# backend/app/api/endpoints/admin.py
from fastapi import APIRouter, Depends, HTTPException
from typing import Any
from app.api.deps import require_admin
# An admin-specific supabase client initialized with your secret SERVICE_ROLE_KEY
from app.db.supabase_client import supabase_admin 

router = APIRouter()

@router.post("/admin/invite-staff")
async def invite_staff_member(
    email: str, name: str
    , current_admin: dict[str, Any] = Depends(require_admin)
    ):
    try:
        # 1. Tell Supabase Auth to create a pending user and send an invite email
        invite_response = supabase_admin.auth.admin.invite_user_by_email(email)
        new_user_id = invite_response.user.id
        
        # 2. Automatically seed them into your STAFF table right away
        supabase_admin.table("STAFF").insert({
            "STAFF_ID": new_user_id,
            "STAFF_NAME": name,
            "STAFF_EMAIL": email,
            "ROLE": "manager"
        }).execute()
        
        return {"status": "success", "message": f"Invitation email dispatched to {email}"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))