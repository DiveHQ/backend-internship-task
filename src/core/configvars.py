from pydantic import BaseSettings


class EnvConfig(BaseSettings):
    SECRET: str = "NOT THE REAL SECRET"
    NUTRIXION_APP_ID: str = "NOT REAL APP ID"
    NUTRIXION_APP_KEY: str = "NOT REAL APP KEY"
    API_URL: str = "NOT REAL URL"
    ADMIN_EMAIL: str = "NOT REAL EMAIL"
    ADMIN_FIRST_NAME: str = "NOT REAL FIRST NAME"
    ADMIN_LAST_NAME: str = "NOT REAL LAST NAME"
    PASSWORD: str = "NOT THE REAL PASSWORD"
    PASSWORD_CONFIRMATION: str = "NOT THE REAL PASSWORD CONFIRMATION"

    class Config:
        env_file = ".env"


env_config = EnvConfig()
