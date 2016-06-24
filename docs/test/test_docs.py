import os
import pytest
from pytest import fixture

# configuration

PACKAGE = "knittingpattern"

# constants


def absjoin(*args):
    return os.path.abspath(os.path.join(*args))

HERE = absjoin(os.path.dirname(__file__))
DOCS_DIRECTORY = absjoin(HERE, "..")
PACKAGE_LOCATION = absjoin(DOCS_DIRECTORY, "..")
PACKAGE_ROOT = absjoin(PACKAGE_LOCATION, PACKAGE)
PACKAGE_DOCUMENTATION = absjoin(HERE, "..", "reference")
BUILD_DIRECTORY = absjoin(PACKAGE_LOCATION, "build")
COVERAGE_DIRECTORY = absjoin(BUILD_DIRECTORY, "coverage")
PYTHON_COVERAGE_FILE = absjoin(COVERAGE_DIRECTORY, "python.txt")
