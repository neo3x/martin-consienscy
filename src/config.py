"""Configuration management for the Artificial Consciousness Architecture project.

This module handles all configuration using Pydantic Settings, loading from environment
variables and .env files.
"""

from typing import Literal

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Main configuration settings for the project."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # LLM Configuration
    anthropic_api_key: str

    @field_validator("anthropic_api_key")
    @classmethod
    def validate_api_key(cls, v: str) -> str:
        """Validate that the API key is not empty and has correct format."""
        if not v or not v.strip():
            raise ValueError("ANTHROPIC_API_KEY cannot be empty")
        v = v.strip()
        if not v.startswith("sk-ant-"):
            raise ValueError(
                "ANTHROPIC_API_KEY should start with 'sk-ant-'. "
                "Please check your API key format."
            )
        if len(v) < 20:
            raise ValueError("ANTHROPIC_API_KEY appears to be too short")
        return v

    llm_model: str = "claude-sonnet-4-5-20250929"
    llm_max_tokens: int = 4096
    llm_temperature: float = 0.7

    # Database Configuration
    database_path: str = "data/"
    vector_db_type: Literal["chromadb", "qdrant"] = "chromadb"
    vector_db_path: str = "data/memories/semantic/"

    # Logging Configuration
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = "INFO"
    log_path: str = "data/logs/"

    # System Parameters (Phase 0)
    workspace_capacity: int = 7
    emotional_state_dimensions: int = 5
    memory_consolidation_threshold: float = 0.6

    # Phase Control
    current_phase: int = 0
    enable_metacognition: bool = False
    enable_workspace: bool = False

    # Development
    debug: bool = False
    verbose_logging: bool = False


# Global settings instance
settings = Settings()
