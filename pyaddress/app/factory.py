"""
Title: factory.py
Author: Mateusz Jarek <mateuszjarek.mj@gmail.com>

Description:

    *pyaddress* application setup and configuration.

"""
import logging.config
import pathlib

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.router import root_router
from app.settings import get_settings, initialize_settings


logger_conf = pathlib.Path(__file__).parent / "logging.conf"
logger = logging.getLogger(name="app")
if not pathlib.Path.exists(logger_conf):
    raise FileNotFoundError(f"Missing logger configuration file: {logger_conf}.")
logging.config.fileConfig(logger_conf)


tags_metadata = [
    {
        "name": "Addresses",
        "description": "Multinational address management"
    }
]


def setup_cors(application: FastAPI) -> None:
    """Configure CORS policies"""
    settings = get_settings()
    application.add_middleware(
        CORSMiddleware,
        allow_origins=str.split(settings.CORS_ORIGINS, ","),
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


def create_application(version: str = "CURRENT") -> FastAPI:
    """Create application object and configure its services."""
    initialize_settings()
    settings = get_settings()
    application = FastAPI(
        title="pyaddress service",
        description="*pyaddress* processes addresses from different countries of the world.",
        debug=bool(settings.DEBUG),
        version=version,
        openapi_tags=tags_metadata
    )
    application.include_router(router=root_router)
    setup_cors(application=application)
    return application
