from pydantic_settings import BaseSettings



class AppSettings(BaseSettings):
    APP_NAME: str = "Concierge Service"
    
    AGENT_MODEL: str = "gpt-4o-mini"
    OPENAI_API_KEY: str = ""
    

settings = AppSettings()