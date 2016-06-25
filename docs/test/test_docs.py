import os


def absjoin(*args):
    """
    :return: an absolute path to the joined arguments
    :param args: the parts of the path to join
    """
    return os.path.abspath(os.path.join(*args))

PACKAGE = "knittingpattern"

HERE = absjoin(os.path.dirname(__file__))
DOCS_DIRECTORY = absjoin(HERE, "..")
PACKAGE_LOCATION = absjoin(DOCS_DIRECTORY, "..")
PACKAGE_ROOT = absjoin(PACKAGE_LOCATION, PACKAGE)
PACKAGE_DOCUMENTATION = absjoin(HERE, "..", "reference")
BUILD_DIRECTORY = absjoin(PACKAGE_LOCATION, "build")
COVERAGE_DIRECTORY = absjoin(BUILD_DIRECTORY, "coverage")
PYTHON_COVERAGE_FILE = absjoin(COVERAGE_DIRECTORY, "python.txt")

__all__ = ["PACKAGE", "HERE", "DOCS_DIRECTORY", "PACKAGE_LOCATION",
           "PACKAGE_ROOT", "PACKAGE_DOCUMENTATION", "BUILD_DIRECTORY",
           "COVERAGE_DIRECTORY", "PYTHON_COVERAGE_FILE"]
