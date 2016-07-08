"""Writing objects to files

This module offers a unified interface to serialize objects to strings
and save them to files.
"""
from .file import ContentDumper as ContentDumper
from .json import JSONDumper as JSONDumper
from .xml import XMLDumper as XMLDumper
from .svg import SVGDumper as SVGDumper

__all__ = ["ContentDumper", "JSONDumper", "XMLDumper", "SVGDumper"]
