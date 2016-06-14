"""Convinience methods for conversion

"""


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
    Load.__name__ = load_and_dump.__name__
    Load.__doc__ = load_and_dump.__doc__

    class Dump(Dumper):
        pass
    Dumper.__name__ = load_and_dump.__name__
    Dumper.__doc__ = load_and_dump.__doc__

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

        @decorate_load_and_dump(Loader, Dumper)
        def convert_from_loader_to_dumper(loaded_stuff):
            # convert
            return converted_stuff
    """
    return lambda function: load_and_dump(Loader, Dumper, function,
                                          loader_args, loader_kw,
                                          dumper_args, dumper_kw)


__all__ = ["load_and_dump"]
