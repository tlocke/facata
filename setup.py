#!/usr/bin/env python

from setuptools import setup

import versioneer

long_description = """

Facata
------

A Python library that provides a simplified alternative to DBAPI 2. It provides
a facade in front of DBAPI 2 drivers.
"""

cmdclass = dict(versioneer.get_cmdclass())
version = versioneer.get_version()

setup(
    name="facata",
    maintainer="Tony Locke",
    maintainer_email="tlocke@tlocke.org.uk",
    version=version,
    cmdclass=cmdclass,
    description="A simplified alternative to DBAPI 2.",
    long_description=long_description,
    url="https://github.com/tlocke/facata",
    license="MIT",
    python_requires=">=3.6",
    install_requires=[],
    extras_require={
        "mariadb": "mariadb>=1.0.7",
        "pg8000": "pg8000>=1.21.0",
        "psycopg2": "psycopg2-binary>=2.9.1",
        "mysql-connector": "mysql-connector-python>=8.0.26",
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: Implementation",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: Jython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords="DBAPI database SQL",
    packages=("facata",),
)
