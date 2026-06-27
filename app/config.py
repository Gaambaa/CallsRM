from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "CallsRM"
    database_url: str
    #Optional: CallsRM can work without n8n, but if you want to use n8n integration, set the webhook URL here.
    n8n_webhook_url: str = ""

    class Config:
        env_file = ".env"