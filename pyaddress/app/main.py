"""
Title: main.py
Author: Mateusz Jarek <mateuszjarek.mj@gmail.com>

Description:

    *pyaddress* service entrypoint.

"""
from app.factory import create_application
from app.version import VERSION


app = create_application(version=VERSION)
