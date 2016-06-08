#
# see https://pytest.org/latest/goodpractices.html
# for why this module exists
#

from pytest import fixture, raises
from unittest.mock import MagicMock
import os
import sys
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))
