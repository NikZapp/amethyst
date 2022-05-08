#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from setuptools import setup


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="amethyst-plugin",
    version="1.0",
    description="A small, event based plugin system written in python.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="NikZapp",
    url="http://github.com/nikzapp/amethyst",
    py_modules=["amethyst"],
    entry_points={"console_scripts": ["amethyst = amethyst:main"]},
)
