"""
Application configuration settings
"""

from pydantic_settings import BaseSettings
from typing import Optional
import os


class Settings(BaseSettings):
    """Application settings"""
    
    # Application
    app_name: str = "Restaurant Seating System API"
    app_version: str = "1.0.0"
    debug: bool = False
    
    # API
    api_v1_prefix: str = "/api/v1"
    host: str = "0.0.0.0"
    port: int = 8000
    
    # Database
    database_url: Optional[str] = None
    database_host: str = "localhost"
    database_port: int = 3306
    database_name: str = "restaurant_seating"
    database_user: str = "restaurant_user"
    database_password: str = "restaurant_password"
    database_echo: bool = False
    
    # Security
    secret_key: str = "your-secret-key-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # CORS
    allowed_origins: list[str] = ["*"]
    allowed_methods: list[str] = ["*"]
    allowed_headers: list[str] = ["*"]
    
    # Logging
    log_level: str = "INFO"
    
    class Config:
        env_file = ".env"
        case_sensitive = False

    @property
    def database_url_computed(self) -> str:
        """Compute database URL from individual components"""
        if self.database_url:
            return self.database_url
        return f"mysql+pymysql://{self.database_user}:{self.database_password}@{self.database_host}:{self.database_port}/{self.database_name}"


# Global settings instance
settings = Settings()
