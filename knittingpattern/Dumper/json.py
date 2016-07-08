"""Dump objects to JSON."""
import json
from .file import ContentDumper


class JSONDumper(ContentDumper):

    """This class can be used to dump object s as JSON."""

    def __init__(self, on_dump):
        """Create a new JSONDumper object with the callable `on_dump`.

        `on_dump` takes no aguments and returns the object that should be
        serialized to JSON."""
        super().__init__(self._dump_to_file)
        self.__dump_object = on_dump

    def object(self):
        """Return the object that should be dumped."""
        return self.__dump_object()

    def _dump_to_file(self, file):
        """dump to the file"""
        json.dump(self.object(), file)

    def knitting_pattern(self, specification=None):
        """loads a :class:`knitting pattern
        <knittingpattern.KnittingPattern.KnittingPattern>` from the dumped
        content

        :param specification: a
          :class:`~knittingpattern.ParsingSpecification.ParsingSpecification`
          or :obj:`None` to use the default specification"""
        from ..ParsingSpecification import new_knitting_pattern_set_loader
        if specification is None:
            loader = new_knitting_pattern_set_loader()
        else:
            loader = new_knitting_pattern_set_loader(specification)
        return loader.object(self.object())

__all__ = ["JSONDumper"]
