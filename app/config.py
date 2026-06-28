from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "CallsRM"
    database_url: str
    # Optional: n8n integration
    n8n_webhook_url: str = ""
    # Optional: WhatsApp Business API
    whatsapp_token: str = ""
    whatsapp_phone_number_id: str = ""

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()