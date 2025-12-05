from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str 
    api_key: str = "test-api-key"
    testing: bool = False

    class Config:
        env_file = "../../.env" # Points to the root .env file
