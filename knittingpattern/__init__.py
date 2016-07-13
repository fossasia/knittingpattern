"""The knitting pattern module.

Load and convert knitting patterns using the convinience functions lited below.
"""
# there should be no imports

#: the version of the knitting pattern library
__version__ = '0.1.9'

#: an empty knitting pattern set as specification
EMPTY_KNITTING_PATTERN_SET = {"version": "0.1", "type": "knitting pattern",
                              "patterns": []}


def load_from():
    """Create a loader to load knitting patterns with.

    :return: the loader to load objects with
    :rtype: knittingpattern.Loader.JSONLoader

    Example:

    .. code:: python

       import knittingpattern, webbrowser
       k = knittingpattern.load_from().example("Cafe.json")
       webbrowser.open(k.to_svg(25).temporary_path(".svg"))

    """
    from .ParsingSpecification import new_knitting_pattern_set_loader
    return new_knitting_pattern_set_loader()


def load_from_object(object_):
    """Load a knitting pattern from an object.

    :rtype: knittingpattern.KnittingPatternSet.KnittingPatternSet
    """
    return load_from().object(object_)


def load_from_string(string):
    """Load a knitting pattern from a string.

    :rtype: knittingpattern.KnittingPatternSet.KnittingPatternSet
    """
    return load_from().string(string)


def load_from_file(file):
    """Load a knitting pattern from a file-like object.

    :rtype: knittingpattern.KnittingPatternSet.KnittingPatternSet
    """
    return load_from().file(file)


def load_from_path(path):
    """Load a knitting pattern from a file behind located at `path`.

    :rtype: knittingpattern.KnittingPatternSet.KnittingPatternSet
    """
    return load_from().path(path)


def load_from_url(url):
    """Load a knitting pattern from a url.

    :rtype: knittingpattern.KnittingPatternSet.KnittingPatternSet
    """
    return load_from().url(url)


def load_from_relative_file(module, path_relative_to):
    """Load a knitting pattern from a path relative to a module.

    :param str module: can be a module's file, a module's name or
      a module's path.
    :param str path_relative_to: is the path relavive to the modules location.
      The result is loaded from this.

    :rtype: knittingpattern.KnittingPatternSet.KnittingPatternSet
    """
    return load_from().relative_file(module, path_relative_to)


def convert_from_image(colors=("white", "black")):
    """Convert and image to a knitting pattern.

    :return: a loader
    :rtype: knittingpattern.Loader.PathLoader
    :param tuple colors: the colors to convert to

    .. seealso:: :mod:`knittingoattern.convert.image_to_knitting_pattern`
    """
    from .convert.image_to_knittingpattern import \
        convert_image_to_knitting_pattern
    return convert_image_to_knitting_pattern(colors=colors)


def new_knitting_pattern(id_, name=None):
    """Create a new knitting pattern.

    :return: a new empty knitting pattern.
    :param id_: the id of the knitting pattern
    :param name: the name of the knitting pattern or :obj:`None` if the
      :paramref:`id_` should be used
    :rtype: knittingpattern.KnittingPattern.KnittingPattern

    .. seealso:: :meth:`KnittingPatternSet.add_new_pattern()
      <knittingpattern.KnittingPatternSet.KnittingPatternSet.add_new_pattern>`
    """
    knitting_pattern_set = new_knitting_pattern_set()
    return knitting_pattern_set.add_new_pattern(id_, name)


def new_knitting_pattern_set():
    """Create a new, empty knitting pattern set.

    :rtype: knittingpattern.KnittingPatternSet.KnittingPatternSet
    :return: a new, empty knitting pattern set
    """
    return load_from_object(EMPTY_KNITTING_PATTERN_SET)

__all__ = ["load_from_object", "load_from_string", "load_from_file",
           "load_from_path", "load_from_url", "load_from_relative_file",
           "convert_from_image", "load_from", "new_knitting_pattern",
           "new_knitting_pattern_set"]
