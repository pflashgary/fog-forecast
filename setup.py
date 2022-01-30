#!/usr/bin/env python

from distutils.core import setup

setup(
    name="Fog-Forecast",
    version="1.0",
    description="Pattern Recognition in NWP model data to enhance visibility classes",
    author="Pegah Flashgary, Nasehe Jamshidpour",
    author_email="pflashgary@gmail.com",
    url="https://github.com/pflashgary/fog-forecast",
    packages=["cartopy", "eccodes", "cfgrib", "xarray[complete]"],
)
