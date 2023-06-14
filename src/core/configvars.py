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
    ERRORS: dict = {
        "INVALID_CREDENTIALS": "Invalid Credentials",
        "PASSWORD_MATCH_DETAIL": "Passwords do not match",
        "USER_EXISTS": "User with email already exists",
        "CALORIE_NOT_FOUND": "Calorie entry not found",
        "USER_NOT_FOUND": "User not found",
        "NOT_PERMITTED_UPDATE_CALORIE": "You are not permitted to update this calorie entry",
        "NOT_PERMITTED_DELETE_CALORIE": "You are not permitted to delete this calorie entry",
        "NOT_PERMITTED_DELETE_USER": "You are not permitted to delete this user",
        "NOT_PERMITTED_UPDATE_USER": "You are not permitted to update this user",
        "NOT_PERMITTED": "You are not permitted to perform this operation",
        "ENTRY_NOT_RETRIEVED": "Could not retrieve number of calories. Enter it or write a new text"

    }

    class Config:
        env_file = ".env"


env_config = EnvConfig()
