#!/usr/bin/python3
"""Test the coverage of documentation.

No function shall be left out by the documentation.
Run this module to create the missing documentation files.

"""
from test_docs import PACKAGE_LOCATION, PACKAGE, PACKAGE_DOCUMENTATION, \
    PACKAGE_ROOT
import pytest
from collections import namedtuple
import os


def relative_module_path(absolute_path):
    relative_path = absolute_path[len(PACKAGE_LOCATION):]
    if not relative_path.startswith(PACKAGE):
        # remove /
        relative_path = relative_path[1:]
    assert relative_path.startswith(PACKAGE)
    return relative_path


def module_name_and_doc(relative_path):
    assert relative_path.startswith(PACKAGE)
    file, ext = os.path.splitext(relative_path)
    assert ext == ".py"
    names = []
    while file:
        file, name = os.path.split(file)
        names.insert(0, name)
    assert names
    if names[-1] == "__init__":
        names.pop(-1)
        doc = names + ["index.rst"]
    else:
        doc = names[:-1] + [names[-1] + ".rst"]
    doc_file = os.path.join(PACKAGE_DOCUMENTATION, *doc)
    return ".".join(names), doc_file


Module = namedtuple("Module", ["absolute_path", "path", "name", "doc_file",
                               "lines", "title"])
MODULES = []


def add_module(absolute_path):
    relative_path = relative_module_path(absolute_path)
    name, doc_path = module_name_and_doc(relative_path)
    if os.path.isfile(doc_path):
        with open(doc_path) as file:
            lines = file.readlines()
    else:
        lines = []
    relative_name = name.rsplit(".", 1)[-1]
    title = ":py:mod:`{}` Module".format(relative_name)
    MODULES.append(Module(absolute_path, relative_path, name, doc_path, lines,
                          title))


for dirpath, dirnames, filenames in os.walk(PACKAGE_ROOT):
    if "__init__.py" not in filenames:
        # only use module content
        continue
    for filename in filenames:
        if filename.endswith(".py"):
            add_module(os.path.join(dirpath, filename))


CREATE_MODULE_MESSAGE = "You can execute {} to create the missing "\
                        "documentation file.".format(__file__)


@pytest.mark.parametrize('module', MODULES)
def test_module_has_a_documentation_file(module):
    assert os.path.isfile(module.doc_file), CREATE_MODULE_MESSAGE


@pytest.mark.parametrize('module', MODULES)
def test_documentation_references_module(module):
    # assert module.lines[0].strip() == ".. py:module:: " + module.name
    assert module.lines[1].strip() == ".. py:currentmodule:: " + module.name


@pytest.mark.parametrize('module', MODULES)
def test_documentation_has_proper_title(module):
    assert module.lines[2].strip() == ""
    assert module.lines[3].strip() == module.title
    assert module.lines[4].strip() == "=" * len(module.title)


def create_new_module_documentation():
    """Create documentation so it fits the tests."""
    for module in MODULES:
        if not os.path.isfile(module.doc_file):
            directory = os.path.dirname(module.doc_file)
            os.makedirs(directory, exist_ok=True)
            with open(module.doc_file, "w") as file:
                write = file.write
                write("\n")  # .. py:module:: " + module.name + "\n")
                write(".. py:currentmodule:: " + module.name + "\n")
                write("\n")
                write(module.title + "\n")
                write("=" * len(module.title) + "\n")
                write("\n")
                write(".. automodule:: " + module.name + "\n")
                write("   :show-inheritance:\n")
                write("   :members:\n")
                write("   :special-members:\n")
                write("\n")


create_new_module_documentation()
