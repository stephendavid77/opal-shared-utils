from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DB_TYPE: str
    DB_NAME: str
    DB_HOST: str = ""
    DB_PORT: int = 0
    DB_USER: str = ""
    DB_PASSWORD: str = ""
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_DAYS: int
    GOOGLE_CLIENT_ID: str
    GOOGLE_CLIENT_SECRET: str
    GOOGLE_REDIRECT_URI: str
    AUTH_SERVICE_PORT: int = 8000
    SHARED_BACKEND_PORT: int = 8001

    class Config:
        env_file = "../.env"


settings = Settings()
