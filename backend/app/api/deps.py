import jwt
from jwt import PyJWKClient
from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional, Any
from app.config import configs

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

def require_admin(
    current_user: dict[str, Any] = Depends(get_current_user)
) -> dict[str, Any]:
    if current_user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Admins only.")
    return current_user