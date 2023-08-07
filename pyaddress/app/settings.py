"""
Title: settings.py
Author: Mateusz Jarek <mateuszjarek.mj@gmail.com>

Description:

    *pyaddress* configuration management.

"""
from pydantic_settings import BaseSettings


_SETTINGS = None


class Settings(BaseSettings):

    DEBUG: bool = True
    CORS_ORIGINS: str = "http://localhost:8080,http://127.0.0.1:8080"


def initialize_settings() -> None:
    """
    Initialize runtime configuration based on values inherited from environment variables
    or read from "env" file.
    """
    global _SETTINGS  # pylint: disable=global-statement
    if _SETTINGS is not None:
        return
    _SETTINGS = Settings()


def get_settings() -> Settings:
    """Return application settings instance."""
    if _SETTINGS is None:
        raise RuntimeError("Runtime configuration has not been initialized yet.")
    return _SETTINGS  # noqa
