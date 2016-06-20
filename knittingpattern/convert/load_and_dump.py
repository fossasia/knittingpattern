"""Convinience methods for conversion

"""


def _copy_attributes(from_function, to_class):
    to_class.__name__ = from_function.__name__
    to_class.__doc__ = from_function.__doc__
    to_class.__qualname__ = from_function.__qualname__
    to_class.__module__ = from_function.__module__


def load_and_dump(Loader, Dumper, load_and_dump,
                  loader_args=(), loader_kw={},
                  dumper_args=(), dumper_kw={}):
    """Returns a loader instance that first loads an the dumps.

    The arguments of both, Loader and Dumper will be passed to `load_and_dump`.
    The return value of `load_and_dump` is passed to the Dumper.

    The resulting loader Object has the doc string of `load_and_dump`.
    """

    class Load(Loader):
        pass
    _copy_attributes(load_and_dump, Load)

    class Dump(Dumper):
        pass
    _copy_attributes(load_and_dump, Dump)

    def load(*args1, **kw):
        """return the dumper"""
        def dump(*args2, **kw2):
            kw.update(kw2)
            return load_and_dump(*(args1 + args2), **kw)
        return Dump(dump, *dumper_args, **dumper_kw)
    return Load(load, *loader_args, **loader_kw)


def decorate_load_and_dump(Loader, Dumper,
                           loader_args=(), loader_kw={},
                           dumper_args=(), dumper_kw={}):
    """Same as `load_and_dump()` but returns a function to enable decorator
    syntax.

    Examples:

        @decorate_load_and_dump(ContentLoader, JSONDumper)
        def convert_from_loader_to_dumper(loaded_stuff):
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


__all__ = ["load_and_dump"]
