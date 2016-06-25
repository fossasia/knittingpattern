#
# see https://pytest.org/latest/goodpractices.html
# for why this module exists
#
from pytest import fixture, raises, fail
from unittest.mock import MagicMock, call
import pytest
import os
import sys
import io
try:
    import untangle  # http://docs.python-guide.org/en/latest/scenarios/xml/
except ImportError:
    raise ImportError("Install untangle with \"{} -m pip install untangle\"."
                      "".format(sys.executable))

HERE = os.path.dirname(__file__)

sys.path.insert(0, os.path.join(HERE, "../../.."))


def parse_file(file):
    parser = untangle.make_parser()
    sax_handler = untangle.Handler()
    parser.setContentHandler(sax_handler)
    parser.parse(file)
    return sax_handler.root


def parse_string(string):
    file = io.StringIO()
    file.write(string)
    file.seek(0)
    return parse_file(file)


__all__ = ["HERE", "parse_string", "parse_file", "pytest", "fixture", "raises",
           "fail", "MagicMock", "call", "untangle", "os", "sys", "io"]
