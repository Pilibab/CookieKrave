# config.py
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, SecretStr
from pathlib import Path

# Traces from config.py -> app/ -> backend/ -> CookieKrave/
ROOT_DIR = Path(__file__).resolve().parent.parent.parent
ENV_PATH = ROOT_DIR / ".env"

class AppConfig(BaseSettings):
    # ? why tf fo i need default=none here???
    SUPABASE_KEY: SecretStr = Field(alias="SUPABASE_KEY")
    SUPABASE_URL: SecretStr = Field(alias="SUPABASE_URL")
    DATABASE_URL: SecretStr = Field(alias="DATABASE_URL")
    SUPABASE_KEY_ADMIN: SecretStr = Field(alias="SUPABASE_KEY_ADMIN")
    DIRECT_URL: SecretStr = Field(alias="DIRECT_URL")
    
    # change this this is just a template 
    # backend_url: str = Field(default="http://localhost:5000", alias="BACKEND_URL")
    # frontend_url: str = Field(alias="FRONTEND_URL")

    model_config = SettingsConfigDict(
        env_file=ENV_PATH,
        extra="ignore", 
        env_ignore_empty=True   # ignore empty env var
        )

# dont remove the comment if u want pydantic to work 
# idk why its raising an error despite the AppConfig working 
configs = AppConfig() # type: ignore 

