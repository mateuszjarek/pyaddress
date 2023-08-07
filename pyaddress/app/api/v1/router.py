"""
Title: router.py
Author: Mateusz Jarek <mateuszjarek.mj@gmail.com>

Description:

    *pyaddress* API version 1.0 child router definition.

"""
from fastapi.routing import APIRouter

from app.api.v1.endpoints.addresses import address_router


ROUTER_PATH = "/api/v1"


v1_router = APIRouter(prefix="/api/v1")
v1_router.include_router(router=address_router, tags=["Addresses"])
