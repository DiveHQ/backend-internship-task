from pydantic import BaseSettings


class EnvConfig(BaseSettings):
    SECRET: str = "NOT THE REAL SECRET"
    NUTRIXION_APP_ID: str = "NOT REAL APP ID"
    NUTRIXION_APP_KEY: str = "NOT REAL APP KEY"
    URL: str = "NOT REAL URL"

    class Config:
        env_file = ".env"


env_config = EnvConfig()
