from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SENTRY_DSN: str
    SQLALCHEMY_DATABASE_URL: str

    class Config:
        env_file = ".env"

settings = Settings()