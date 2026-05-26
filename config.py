from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    TELEGRAM_BOT_TOKEN: str
    TOGETHER_API_KEY: str
    ENVIRONMENT: str = "production"
    DEFAULT_MODEL: str = "black-forest-labs/FLUX.1-schnell"
    
    model_config = SettingsConfigDict(
        env_file=".env", 
        env_file_encoding="utf-8", 
        extra="ignore"
    )

settings = Settings()
