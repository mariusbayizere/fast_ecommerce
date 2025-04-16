from pydantic_settings import BaseSettings, SettingsConfigDict
import os


class Settings(BaseSettings):
    DATABASE_URL: str


    model_config = SettingsConfigDict(
        # env_file='.env',
        env_file=os.path.join(os.path.dirname(__file__), 'students/.env'),
        env_file_encoding='utf-8',
        extra='ignore'
    )

Config = Settings()