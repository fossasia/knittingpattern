"""convinience methods for conversion

Best to use :meth:`decorate_load_and_dump`.

"""
from functools import wraps


def load_and_dump(Loader, Dumper, load_and_dump,
                  loader_args=(), loader_kw={},
                  dumper_args=(), dumper_kw={}):
    """:return: a function that has the doc string of :paramref:`load_and_dump`
      additional arguments to this function are passed on to
      :paramref:`load_and_dump`.

    :param Loader: a loader, e.g. :class:`knittingpattern.Loader.PathLoader`
    :param tuple loader_args: additional arguments for the creation of the
      :paramref:`Loader`
    :param dict loader_kw: additional keyword arguments for the creation of the
      :paramref:`Loader`
    :param Dumper: a loader, e.g. :class:`knittingpattern.Dumper.ContentDumper`
    :param tuple dumper_args: additional arguments for the creation of the
      :paramref:`Dumper`
    :param dict dumper_kw: additional keyword arguments for the creation of the
      :paramref:`Dumper`
    :param load_and_dump: a function to call with the loaded content.
      The arguments of both, :paramref:`Loader` and :paramref:`Dumper`
      will be passed to :paramref:`load_and_dump`.
      Any additional arguments to the return value are also passed to
      :paramref:`load_and_dump`.
      The return value of :paramref:`load_and_dump` is passed back to the
      :paramref:`Dumper`.

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
    """Same as :func:`load_and_dump` but returns a function to enable decorator
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
