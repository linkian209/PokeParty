from pydantic import BaseSettings

class Settings(BaseSettings):
    client_secret: str
    client_id: str
    database_url: str = "sqlite:///./pokeparty.db"
    
    class Config:
        env_file = ".env"