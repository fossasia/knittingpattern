"""This module holds the common test code.

.. seealso:: `pytest good practices
  <https://pytest.org/latest/goodpractices.html>`__ for why this module exists.
"""
from pytest import fixture, raises
from unittest.mock import MagicMock
import os
import sys
import pytest

# sys.path makes knittingpattern importable
HERE = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(HERE, "../.."))

__all__ = ["fixture", "raises", "MagicMock", "os", "sys", "pytest"]
