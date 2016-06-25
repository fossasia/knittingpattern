from test_docs import BUILD_DIRECTORY, DOCS_DIRECTORY, PYTHON_COVERAGE_FILE
import subprocess
import re
import shutil
import pytest
from pytest import fixture
import os


UNDOCUMENTED_PYTHON_OBJECTS = """Undocumented Python objects
===========================
"""
WARNING_PATTERN = b"(?:checking consistency\\.\\.\\. )?" \
                  b"(.*(?:WARNING|SEVERE|ERROR):.*)"


def print_bytes(bytes_):
    try:
        print(bytes_.decode())
    except UnicodeDecodeError:
        print(bytes_)


@fixture(scope="module")
def sphinx_build():
    if os.path.exists(BUILD_DIRECTORY):
        shutil.rmtree(BUILD_DIRECTORY)
    output = subprocess.check_output(
            "make html", shell=True, cwd=DOCS_DIRECTORY,
            stderr=subprocess.STDOUT
        )
    output += subprocess.check_output(
            "make coverage", shell=True, cwd=DOCS_DIRECTORY,
            stderr=subprocess.STDOUT
        )
    print(output.decode())
    return output


@fixture(scope="module")
def coverage(sphinx_build):
    assert sphinx_build, "we built before we try to access the result"
    with open(PYTHON_COVERAGE_FILE) as f:
        return f.read()


@fixture
def warnings(sphinx_build):
    return re.findall(WARNING_PATTERN, sphinx_build)


def test_all_methods_are_documented(coverage):
    print(coverage)
    assert coverage == UNDOCUMENTED_PYTHON_OBJECTS


def test_doc_build_passes_without_warnings(warnings):
    #  WARNING: document isn't included in any toctree
    for warning in warnings:
        print_bytes(warning.strip())
    assert warnings == []
