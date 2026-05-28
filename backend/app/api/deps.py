import jwt
from jwt import PyJWKClient
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.config import configs  # import configs, not os.environ

security = HTTPBearer()

# fetch the correct key to be decoded 
# ! correct way to get the public api key from ES256
jwks_client = PyJWKClient(
    f"{configs.SUPABASE_URL.get_secret_value()}/auth/v1/keys"
)

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):  # was bearer_scheme
    """decodes jwt token to get the payload"""
    token = credentials.credentials
    try:
        signing_key = jwks_client.get_signing_key_from_jwt(token)
        payload = jwt.decode(
            token,
            signing_key.key,  
            algorithms=["HS256", "ES256"],                      # ! supabase uses "ES256" for encryption
            options={"verify_aud": False}
        )
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired.")
    except jwt.InvalidTokenError as e:
        raise HTTPException(status_code=401, detail=f"Invalid token: {e}")

def require_admin(current_user: dict[str, str | None] = Depends(get_current_user)):
    if current_user.get("role") != "admin":  # .get() is safer than []
        raise HTTPException(status_code=403, detail="Admins only.")
    return current_user