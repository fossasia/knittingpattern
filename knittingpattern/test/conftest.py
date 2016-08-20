"""This module holds the common test code.

.. seealso:: `pytest good practices
  <https://pytest.org/latest/goodpractices.html>`__ for why this module exists.
"""
import os
import sys

# sys.path makes knittingpattern importable
HERE = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(HERE, "../.."))
__builtins__["HERE"] = HERE
