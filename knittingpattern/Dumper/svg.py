"""Dump objects to SVG."""
from .xml import XMLDumper


class SVGDumper(XMLDumper):

    """This class dumps objects to SVG."""

    def kivy_svg(self):
        """An SVG object.

        :return: an SVG object
        :rtype: kivy.graphics.svg.SVG
        :raises ImportError: if the module was not found
        """
        from kivy.graphics.svg import SVG
        with self.temporary_file() as temporary_file:
            return SVG(temporary_file.name)

__all__ = ["SVGDumper"]
