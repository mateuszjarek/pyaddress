#!/usr/bin/env python3
"""
Title: runlocal.py
Author: Mateusz Jarek <mateuszjarek.mj@gmail.com>

Description:

    `pyaddress` startup script for local development.

"""
import os

import uvicorn


def run() -> None:
    """Run local instance within uvicorn process."""
    os.environ["CORS_ORIGINS"] = "http://localhost:8080"
    uvicorn.run(
        "app.main:app",
        host="127.0.0.1",
        port=8080,
        reload=True,
        log_config="app/logging.conf",
    )


if __name__ == "__main__":
    run()
