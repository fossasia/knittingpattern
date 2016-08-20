"""Code common to all test in this directory."""
import os
import sys

# sys.path makes knittingpattern importable
HERE = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(HERE, "../.."))
