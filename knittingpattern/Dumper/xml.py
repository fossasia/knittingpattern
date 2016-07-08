"""Dump objects to XML."""
import xmltodict
from .file import ContentDumper


class XMLDumper(ContentDumper):

    """Used to dump objects as XML."""

    def __init__(self, on_dump):
        """Create a new XMLDumper object with the callable `on_dump`.

        `on_dump` takes no aguments and returns the object that should be
        serialized to XML."""
        super().__init__(self._dump_to_file)
        self.__dump_object = on_dump

    def object(self):
        """Return the object that should be dumped."""
        return self.__dump_object()

    def _dump_to_file(self, file):
        """dump to the file"""
        xmltodict.unparse(self.object(), file, pretty=True)

__all__ = ["XMLDumper"]
