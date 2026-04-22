from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, SecretStr

class AppConfig(BaseSettings):
    # ? why tf fo i need default=none here???
    SUPABASE_KEY: SecretStr = Field(alias="SUPABASE_KEY")
    SUPABASE_URL: SecretStr = Field(alias="SUPABASE_URL")
    DATABASE_URL: SecretStr = Field(alias="DATABASE_URL")
    DIRECT_URL: SecretStr = Field(alias="DIRECT_URL")
    
    # change this this is just a template 
    # backend_url: str = Field(default="http://localhost:5000", alias="BACKEND_URL")
    # frontend_url: str = Field(alias="FRONTEND_URL")

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore", 
        env_ignore_empty=True   # ignore empty env var
        )

# dont remove the comment if u want pydantic to work 
# idk why its raising an error despite the AppConfig working 
configs = AppConfig() # type: ignore 

