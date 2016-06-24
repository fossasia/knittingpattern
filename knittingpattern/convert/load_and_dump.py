"""convinience methods for conversion

"""
from functools import wraps


def load_and_dump(Loader, Dumper, load_and_dump,
                  loader_args=(), loader_kw={},
                  dumper_args=(), dumper_kw={}):
    """Returns a loader instance that first loads an the dumps.

    The arguments of both, Loader and Dumper will be passed to `load_and_dump`.
    The return value of `load_and_dump` is passed to the Dumper.

    The resulting loader Object has the doc string of `load_and_dump`.
    """
    @wraps(load_and_dump)
    def create_loader(*args, **kw1):
        def load(*args1, **kw):
            """return the dumper"""
            def dump(*args2, **kw2):
                kw.update(kw2)
                kw.update(kw1)
                return load_and_dump(*(args + args1 + args2), **kw)
            return Dumper(dump, *dumper_args, **dumper_kw)
        return Loader(load, *loader_args, **loader_kw)
    return create_loader


def decorate_load_and_dump(Loader, Dumper,
                           loader_args=(), loader_kw={},
                           dumper_args=(), dumper_kw={}):
    """Same as `load_and_dump()` but returns a function to enable decorator
    syntax.

    Examples:

    .. code:: Python

        @decorate_load_and_dump(ContentLoader, JSONDumper)
        def convert_from_loader_to_dumper(loaded_stuff, other="arguments"):
            # convert
            return converted_stuff

        @decorate_load_and_dump(PathLoader, ContentDumper)
        def convert_from_loader_to_dumper(loaded_stuff, to_file):
            # convert
            to_file.write(converted_stuff)

    """
    return lambda function: load_and_dump(Loader, Dumper, function,
                                          loader_args, loader_kw,
                                          dumper_args, dumper_kw)


__all__ = ["load_and_dump", "decorate_load_and_dump"]
