from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()


class AppConfig(BaseSettings):
    APP_NAME: str
    APP_PATH: str
    APP_URL: str
    APP_VERSION: str
    DEBUG: bool

    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_NAME: str
    POSTGRES_ECHO: str

    REDIS_PASSWORD: str
    REDIS_HOST: str

    class Config:
        env_file = ".env"


settings_app = AppConfig()
