from pydantic_settings import BaseSettings, SettingsConfigDict
import os


class Settings(BaseSettings):
    DATABASE_URL: str
    DATABASE_URLs: str
    JWT_SECRETE: str
    JWT_ALGORITHM: str
    RADIS_HOST: str = "localhost"
    RADIS_PORT: int = 6379



    model_config = SettingsConfigDict(
        # env_file='.env',
        env_file=os.path.join(os.path.dirname(__file__), 'students/.env'),
        env_file_encoding='utf-8',
        extra='ignore'
    )

Config = Settings()