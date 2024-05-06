import os
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache

class Settings(BaseSettings):
    API_MYSQL_HOSTNAME: str = Field(...,validation_alias="API_MYSQL_HOSTNAME")
    API_MYSQL_PORT: str = Field(...,validation_alias="API_MYSQL_PORT")
    API_MYSQL_USERNAME: str = Field(...,validation_alias="API_MYSQL_USERNAME")
    API_MYSQL_PASSWORD: str = Field(...,validation_alias="API_MYSQL_PASSWORD")

    model_config = SettingsConfigDict(env_file=".env")
    
@lru_cache()
def get_settings():
    return Settings()