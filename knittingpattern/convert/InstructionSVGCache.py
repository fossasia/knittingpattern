"""This module provides functionality to cache instruction SVGs."""
from .InstructionToSVG import default_instructions_to_svg
from ..Dumper import SVGDumper
from copy import deepcopy
from collections import namedtuple

_InstructionId = namedtuple("_InstructionId", ["type", "hex_color"])


class InstructionSVGCache(object):

    """This class is a cache for SVG instructions.

    If you plan too use only :meth:`instruction_to_svg_dict`, you are save to
    replace a
    :class:`knittingpsttern.convert.InstructionToSVG.InstructionToSVG` with
    this cache to get faster results.
    """

    def __init__(self, instruction_to_svg=None):
        """Create the InstructionSVGCache.

        :param instruction_to_svg: an
         :class:`~knittingpattern.convert.InstructionToSVG.InstructionToSVG`
         object. If :obj:`None` is given, the
         :func:`default_instructions_to_svg
         <knittingpattern.convert.InstructionToSVG.default_instructions_to_svg>`
         is used.
        """
        if instruction_to_svg is None:
            instruction_to_svg = default_instructions_to_svg()
        self._instruction_to_svg_dict = \
            instruction_to_svg.instruction_to_svg_dict
        self._cache = {}

    def get_instruction_id(self, instruction_or_id):
        """The id that identifies the instruction in this cache.

        :param instruction_or_id: an :class:`instruction
          <knittingpattern.Instruction.Instruction>` or an instruction id
        :return: a :func:`hashable <hash>` object
        :rtype: tuple
        """
        if isinstance(instruction_or_id, tuple):
            return _InstructionId(instruction_or_id)
        return _InstructionId(instruction_or_id.type,
                              instruction_or_id.hex_color)

    def _new_svg_dumper(self, on_dump):
        """Create a new SVGDumper with the function ``on_dump``.

        :rtype: knittingpattern.Dumper.SVGDumper
        """
        return SVGDumper(on_dump)

    def to_svg(self, instruction_or_id,
               i_promise_not_to_change_the_result=False):
        """Return the SVG for an instruction.

        :param instruction_or_id: either an
          :class:`~knittingpattern.Instruction.Instrucution` or an id
          returned by :meth:`get_instruction_id`
        :param bool i_promise_not_to_change_the_result:

          - :obj:`False`: the result is copied, you can alter it.
          - :obj:`True`: the result is directly from the cache. If you change
            the result, other calls of this function get the changed result.

        :return: an SVGDumper
        :rtype: knittingpattern.Dumper.SVGDumper
        """
        return self._new_svg_dumper(lambda: self.instruction_to_svg_dict(
            instruction_or_id, not i_promise_not_to_change_the_result))

    def instruction_to_svg_dict(self, instruction_or_id, copy_result=True):
        """Return the SVG dict for the SVGBuilder.

        :param instruction_or_id: the instruction or id, see
          :meth:`get_instruction_id`
        :param bool copy_result: whether to copy the result
        :rtype: dict

        The result is cached.
        """
        instruction_id = self.get_instruction_id(instruction_or_id)
        if instruction_id in self._cache:
            result = self._cache[instruction_id]
        else:
            result = self._instruction_to_svg_dict(instruction_id)
            self._cache[instruction_id] = result
        if copy_result:
            result = deepcopy(result)
        return result


def default_instruction_svg_cache():
    """Return the default InstructionSVGCache.

    :rtype: knittingpattern.convert.InstructionSVGCache.InstructionSVGCache
    """
    global _default_instruction_svg_cache
    if _default_instruction_svg_cache is None:
        _default_instruction_svg_cache = InstructionSVGCache()
    return _default_instruction_svg_cache
_default_instruction_svg_cache = None
default_svg_cache = default_instruction_svg_cache

__all__ = ["InstructionSVGCache", "default_instruction_svg_cache",
           "default_svg_cache"]
