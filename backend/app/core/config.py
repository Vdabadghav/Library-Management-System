"""
Configuration management for the application using Pydantic Settings
"""
from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import field_validator, computed_field, Field


class Settings(BaseSettings):
    """Application configuration settings loaded from .env file"""

    # API Configuration
    API_TITLE: str = "Library Management System API"
    API_VERSION: str = "1.0.0"
    API_DESCRIPTION: str = "Complete REST API for Library Management System"

    # Server Configuration
    SERVER_HOST: str = "0.0.0.0"
    SERVER_PORT: int = 8000
    DEBUG: bool = True

    # Database Configuration
    MYSQL_HOST: str = "localhost"
    MYSQL_PORT: int = 3306
    MYSQL_USER: str = "root"
    MYSQL_PASSWORD: str = ""
    MYSQL_DATABASE: str = "library_management_db"

    # JWT & Authentication
    SECRET_KEY: str = "your-secret-key-change-this-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # CORS
    FRONTEND_URL: str = "http://localhost:5173"
    allowed_origins_env: str = Field(
        default="http://localhost:5173,http://localhost:3000,http://localhost:8000",
        validation_alias="ALLOWED_ORIGINS"
    )

    @computed_field
    @property
    def ALLOWED_ORIGINS(self) -> List[str]:
        """Parse ALLOWED_ORIGINS from comma-separated string"""
        return [origin.strip() for origin in self.allowed_origins_env.split(",") if origin.strip()]

    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "logs/app.log"

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
        json_schema_extra={
            "ALLOWED_ORIGINS": "Comma-separated list of allowed origins"
        }
    )

    @property
    def database_url(self) -> str:
        """Construct MySQL database URL"""
        return (
            f"mysql+mysqlconnector://{self.MYSQL_USER}:{self.MYSQL_PASSWORD}"
            f"@{self.MYSQL_HOST}:{self.MYSQL_PORT}/{self.MYSQL_DATABASE}"
        )


# Create settings instance
settings = Settings()
