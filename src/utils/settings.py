from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env",extra="ignore")
    db_connection: str
    SECRET_KEY: str
    ALGORITHM: str
    exp_time: int

settings = Settings()    
