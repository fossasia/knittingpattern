# there should be no imports

__version__ = '0.0.8'


def _load():
    """Returns the loader of a KnittingContext to load objects from."""
    from .KnittingContext import KnittingContext
    return KnittingContext().load


def load_from_object(object):
    """Load a knitting pattern from an object."""
    return _load().object(object)


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

    `module` can be a module, a module's name or a module's path."""
    return _load().relative_file(module, path_relative_to)


__all__ = [
        "load_from_object",
        "load_from_string", "load_from_file", "load_from_path",
        "load_from_url", "load_from_relative_file"
    ]
