from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SENTRY_DSN: str
    SQLALCHEMY_DATABASE_URL: str
    JWT_SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_DAYS: int
    WHATSAPP_TOKEN: str
    PHONE_NUMBER_ID: int

    class Config:
        env_file = ".env"

settings = Settings()