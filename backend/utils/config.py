"""
Configuration loading from environment variables.

Uses Pydantic Settings for type-safe configuration with validation.
Loads from .env or environment variables.

Owner: Sahil Kumar Gupta
"""

from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables or .env file.
    
    Example .env:
        DATABASE_URL=postgresql://user:pass@localhost:5432/diabetescare
        JWT_SECRET=your-secret-key-here
        API_BASE_URL=http://localhost:8000
        LOG_LEVEL=INFO
        CORS_ORIGINS=http://localhost:3000,http://localhost:5173
    """
    
    # Database
    DATABASE_URL: str = "postgresql://diabetescare:diabetescare@localhost:5432/diabetescare"
    SQL_ECHO: bool = False  # Log SQL queries (debug)
    
    # JWT Authentication
    JWT_SECRET: str = "your-secret-key-here-CHANGE-IN-PRODUCTION"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRATION_HOURS: int = 24
    
    # API Configuration
    API_BASE_URL: str = "http://localhost:8000"
    API_TITLE: str = "DiabetesCare AI API"
    API_VERSION: str = "0.1.0"
    API_DESCRIPTION: str = "Inference and research API for diabetic complication detection"
    
    # CORS
    CORS_ORIGINS: str = "http://localhost:3000,http://localhost:5173,http://localhost:8081"
    CORS_CREDENTIALS: bool = True
    CORS_METHODS: str = "GET,POST,PUT,DELETE,PATCH,OPTIONS"
    CORS_HEADERS: str = "Content-Type,Authorization"
    
    # Logging
    LOG_LEVEL: str = "INFO"
    
    # Privacy & Compliance (DPDP Act 2023)
    DATA_LOCALISATION_REGION: str = "Mumbai"  # India only
    K_ANONYMITY_THRESHOLD: int = 5  # Minimum group size for export
    AUDIT_LOG_RETENTION_DAYS: int = 365 * 7  # 7 years (medical records)
    
    # File Upload
    MAX_UPLOAD_SIZE_MB: int = 50  # Max image size
    UPLOAD_DIR: str = "./uploads"  # Relative to project root
    
    # Feature Flags
    ENABLE_INFERENCE: bool = True
    ENABLE_ANONYMISATION: bool = True
    ENABLE_EXPORT: bool = True
    ENABLE_TELECONSULT: bool = False  # Week 5+
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


# Singleton instance
settings = Settings()


def get_settings() -> Settings:
    """Get settings instance (for dependency injection)."""
    return settings


def get_cors_origins() -> list[str]:
    """Parse CORS_ORIGINS string into list."""
    return [origin.strip() for origin in settings.CORS_ORIGINS.split(",")]


# Validation examples (uncomment for debugging)
# if __name__ == "__main__":
#     print(f"Database: {settings.DATABASE_URL}")
#     print(f"JWT Secret length: {len(settings.JWT_SECRET)}")
#     print(f"CORS Origins: {get_cors_origins()}")
