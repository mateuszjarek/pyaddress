"""
Title: addresses.py
Author: Mateusz Jarek <mateuszjarek.mj@gmail.com>

Description:

    Address management API endpoints.

"""
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException

from app.schemas.address import Address
from app.services.address import AddressService, AddressServiceError, get_address_service


address_router = APIRouter(tags=["Addresses"])


@address_router.get("/addresses/extract/address}")
def extract_address_components(
        address: str, address_service: AddressService = Depends(get_address_service)
) -> Optional[Address]:
    """
    Extracts street and number from address string and return as a separate values.
    """
    try:
        return address_service.extract_address_components(address)
    except AddressServiceError:
        raise HTTPException(
            status_code=404,
            detail=f"Could not extract street and number from {address}"
        )
