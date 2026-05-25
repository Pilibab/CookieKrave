import jwt
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.config import configs  # import configs, not os.environ

security = HTTPBearer()

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):  # was bearer_scheme
    token = credentials.credentials
    try:
        payload = jwt.decode(
            token,
            configs.SUPABASE_JWT_SECRET.get_secret_value(),  # unwrap SecretStr
            algorithms=["HS256"],
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