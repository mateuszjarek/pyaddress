"""
Title: router.py
Author: Mateusz Jarek <mateuszjarek.mj@gmail.com>

Description:

    *pyaddress* API root router definition.

"""
from fastapi.routing import APIRouter

from app.api.v1.router import v1_router


root_router = APIRouter()
root_router.include_router(v1_router)
