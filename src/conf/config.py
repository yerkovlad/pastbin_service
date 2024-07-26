from pydantic import ConfigDict, field_validator
from pydantic_settings import BaseSettings
from fastapi.templating import Jinja2Templates


class Settings(BaseSettings):
    BASE_URL: str = "http://127.0.0.1:8000"
    DB_USERS_INFO: str = "your_mongodb"
    DB_FREE_URLS: str = "your_mongodb"
    DB_TEXT_USER: str = "your_mongodb"
    ALGORITHM: str = "HS256"
    MAIL_USERNAME: str = "mail_username"
    MAIL_PASSWORD: str = "mail_password"
    MAIL_FROM: str = "mail_username"
    MAIL_PORT: int = 465
    MAIL_SERVER: str = "smtp.mail_server.com"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    SECRET_KEY: str = "your_secret_key"
    TEMPLATES: Jinja2Templates = Jinja2Templates(directory="src/templates")

    @field_validator("ALGORITHM")
    @classmethod
    def validate_algorithm(cls, v):
        """
        Validate the provided JWT algorithm.

        Args:
        - v (str): The algorithm to validate.

        Raises:
        - ValueError: If the provided algorithm is not supported.

        Returns:
        - str: The validated algorithm.
        """
        if v not in ["HS256", "HS512"]:
            raise ValueError("Algorithm not supported")
        return v

    model_config = ConfigDict(extra="ignore", env_file=".env", env_file_encoding="utf-8")


config = Settings()