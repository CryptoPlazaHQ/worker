from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"  # Ignore environment variables not explicitly defined as fields
    ) 
    
    database_url: str = Field(validation_alias='API_DATABASE_URL')
    api_key: str = Field(validation_alias='API_KEY')
    testing: bool = Field(default=False, validation_alias='TESTING')
    access_token_expire_minutes: int = 30
    algorithm: str = Field(validation_alias='ALGORITHM')
    secret_key: str = Field(validation_alias='SECRET_KEY')
