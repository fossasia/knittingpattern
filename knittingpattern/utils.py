"""This module contains some useful functions.

The functions work on the standard library or are not specific to
a certain existing module.
"""


def unique(iterables):
    """Create an iterable from the iterables that contains each element once.

    :return: an iterable over the iterables. Each element of the result
      appeared only once in the result. They are ordered by the first
      occurrence in the iterables.
    """
    included_elements = set()

    def included(element):
        result = element in included_elements
        included_elements.add(element)
        return result
    return [element for elements in iterables for element in elements
            if not included(element)]


__all__ = ["unique"]
