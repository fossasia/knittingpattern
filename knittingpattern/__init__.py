"""The knitting pattern module.

Load and convert knitting patterns using the convinience functions lited below.
"""
# there should be no imports

__version__ = '0.0.10'


def _load():
    """:return: the loader to load objects from."""
    from .ParsingSpecification import new_knitting_pattern_set_loader
    return new_knitting_pattern_set_loader()


def load_from_object(object_):
    """Load a knitting pattern from an object."""
    return _load().object(object_)


def load_from_string(string):
    """Load a knitting pattern from a string."""
    return _load().string(string)


def load_from_file(file):
    """Load a knitting pattern from a file-like object."""
    return _load().file(file)


def load_from_path(path):
    """Load a knitting pattern from a file behind located at `path`."""
    return _load().path(path)


def load_from_url(url):
    """Load a knitting pattern from a url."""
    return _load().url(url)


def load_from_relative_file(module, path_relative_to):
    """Load a knitting pattern from a `path_relative_to` a `module`.

    `module` can be a module, a module's name or a module's path.
    """
    return _load().relative_file(module, path_relative_to)


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

__all__ = ["load_from_object", "load_from_string", "load_from_file",
           "load_from_path", "load_from_url", "load_from_relative_file",
           "convert_from_image"]
