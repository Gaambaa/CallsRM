from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "CallsRM"
    database_url: str
    #Optional n8n webhook URL for forwarding events
    n8n_webhook_url: str = ""

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()