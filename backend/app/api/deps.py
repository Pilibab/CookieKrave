# backend/app/api/deps.py
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
# from supabase import Client
from db.supabase_client import supabase  # Reusing your initialized global client

# Instantiates the bearer scheme parser
security = HTTPBearer()

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> dict[str, str | None]:
    """
    Extracts the JWT from the Authorization header and validates it with Supabase.
    Blocks the request if the token is forged, expired, or missing.
    """
    token = credentials.credentials
    try:
        # Ask Supabase if this JWT is valid and who it belongs to
        auth_response = supabase.auth.get_user(token)
        
        if not auth_response or not auth_response.user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials."
            )
        
        # Return the user details (ID, email, metadata) to the endpoint
        return {
            "id": auth_response.user.id,
            "email": auth_response.user.email,
            "role": auth_response.user.role
        }
        
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials with authentication server."
        )