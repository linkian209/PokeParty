from pydantic import BaseSettings

class Settings(BaseSettings):
    client_secret: str
    client_id: str
    callback_url: str = "http://localhost:8080/auth/callback"
    database_url: str = "sqlite:///./pokeparty.db"
    
    class Config:
        env_file = ".env"