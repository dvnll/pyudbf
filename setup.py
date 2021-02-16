from setuptools import setup
import os
import sys


if sys.version_info < (3,5):
    sys.exit("Python < 3.5 is not supported.")

def get_version(version_tuple):
    return ".".join(map(str, version_tuple))

init = os.path.join(
        os.path.dirname(__file__), ".", "", "__init__.py")

version_line = list(
        filter(lambda l: l.startswith("VERSION"), open(init))
)[0]

PKG_VERSION= get_version(eval(version_line.split("=")[-1]))

setup(
        name="pyudbf",
        version=PKG_VERSION,
        description="A python implementation of the UDBF (\"Universal Data Bin File\") data format version 107.",
        license="MIT",
        install_requires=["numpy", "math", "logging", "pprint", "typing", "datetime", "os", "struct"],
)
