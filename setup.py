#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
import setuptools
from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()
setup(
    name="guolei-py3-qunjielong",
    version="1.1.3",
    description="群接龙 API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/guolei19850528/guolei_py3_qunjielong",
    author="guolei",
    author_email="174000902@qq.com",
    license="MIT",
    keywors=["qunjielong", "群接龙"],
    packages=setuptools.find_packages('./'),
    install_requires=[
        "addict",
        "retrying",
        "pydantic",
        "guolei-py3-requests",
        "redis",
        "diskcache"
    ],
    python_requires='>=3.0',
    zip_safe=False
)
