from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "Local RAG App"
    APP_VERSION: str = "0.0.1"

    class Config:
        env_file = ".env"

settings = Settings()
