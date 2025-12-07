from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    database_url: str = Field(validation_alias='API_DATABASE_URL')
    api_key: str = Field(validation_alias='API_KEY')
    testing: bool = Field(default=False, validation_alias='TESTING')
    access_token_expire_minutes: int = 30
    algorithm: str = Field(validation_alias='ALGORITHM')
    secret_key: str = Field(validation_alias='SECRET_KEY')



