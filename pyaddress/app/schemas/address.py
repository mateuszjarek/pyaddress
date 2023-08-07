"""
Title: address.py
Author: Mateusz Jarek <mateuszjarek.mj@gmail.com>

Description:

    Address representation schema.

"""
from pydantic import BaseModel, Field


class Address(BaseModel):
    """Simple address representation."""

    street: str
    house_number: str = Field(..., alias="housenumber")

    class Config:
        """Pydantic related configuration."""

        populate_by_name = True
