import jwt
from jwt import PyJWKClient
from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from supabase.client import Client
from typing import Optional, Any
from app.config import configs
from app.db.supabase_client import supabase
from app.repository.staff_repo import StaffRepository

security = HTTPBearer(auto_error=False) # 🚨 Setting auto_error=False prevents hard crashes when header is missing

jwks_client = PyJWKClient(
    f"{configs.SUPABASE_URL.get_secret_value()}/auth/v1/.well-known/jwks.json"
)

def get_current_user(
    request: Request, # 1. Inject raw request context to search cookies
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)
) -> dict[str, Any] :
    """Decodes JWT token from either the Authorization Header OR fallback Cookies."""
    token = None

    # Step A: Check for explicit Authorization Bearer token header (Callback route context)
    if credentials:
        token = credentials.credentials

        
    # Step B: If missing, fallback to extracted browser tracking cookies (Dashboard components view context)
    if not token:
        token = request.cookies.get("sb-access-token")

    # Step C: If both routes turn up completely blank, fail loudly
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Not authenticated: Missing both authorization token bearer header and matching cookie session state."
        )

    try:
        # Step D: Process and execute the validation checks as normal
        signing_key = jwks_client.get_signing_key_from_jwt(token)
        payload = jwt.decode(
            token,
            signing_key.key,  
            algorithms=["HS256", "ES256"],
            options={"verify_aud": False}
        )
        return payload
        
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired.")
    except jwt.InvalidTokenError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Invalid token: {e}")

def get_supabase():
    """Returns the globally initialized supabase client."""
    return supabase

# Helper to provide the repository instance
def get_staff_repository(supabase_client: Client = Depends(get_supabase)) -> StaffRepository:
    return StaffRepository(supabase_client)

# Base user auth dependency you already have
# (Decodes token and returns payload containing 'email')
# def get_current_user(...) -> dict[str, Any]: ...

def require_admin(
    current_user: dict[str, Any] = Depends(get_current_user),
    staff_repo: StaffRepository = Depends(get_staff_repository)
) -> dict[str, Any]:
    """
    Verifies that the authenticated user's email exists in the 
    public.staff table and possesses the 'admin' role designation.
    """
    # 1. Grab email from the validated Supabase JWT Payload
    user_email = current_user.get("email")
    if not user_email:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid session: Token payload does not contain a verified email address."
        )

    # 2. Query your PostgreSQL staff table via StaffRepository
    staff_member = staff_repo.get_by_email(user_email)
    
    # 3. Reject if they aren't registered in the staff pool at all
    if not staff_member:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access Denied: This account is not registered as a member of staff."
        )

    # 4. Check if their assigned role matches 'admin'
    # Note: Depending on whether your base repo parses into Pydantic or a raw dict, 
    # use staff_member.role or staff_member.get('role'). If it's your model class: staff_member.role
    if getattr(staff_member, "role", None) != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access Denied: Administrative privileges required."
        )

    # Return the current user payload (or you could return the staff_member object)
    return current_user