"""Writing objects to files

This module offers a unified interface to serialize objects to strings
and save them to files.
"""
from io import StringIO, BytesIO
from tempfile import NamedTemporaryFile
import json
import xmltodict
from .FileWrapper import BytesWrapper, TextWrapper


class ContentDumper(object):
    """This class is a unified interface for saving objects.

    The idea is to decouple the place to save to from the process used
    to dump the content.
    We are saving several objects such as patterns and SVGs.
    They should all have the same convinient interface.

    The process of saving something usally requires writing to some file.
    However, users may want to have the result as a string, an open file,
    a file on the hard drive on a fixed or temporary location,
    posted to some url or in a zip file.
    This class should provide for all those needs while providing a uniform
    interface for the dumping.

    """
    def __init__(self, on_dump, text_is_expected=True, encoding="UTF-8"):
        """Create a new dumper object with a function :paramref:`on_dump`

        :param on_dump: a function that takes a file-like object as argument
          and writes content to it.
        :param bool text_is_expected: whether to use text mode
          (:obj:`True`, default) or binary mode (:obj:`False`)
          for :paramref:`on_dump`.

        The dumper calls :paramref:`on_dump` with a file-like object every time
        one of its save methods, e.g. :meth:`string` or :meth:`file` is called.
        The file-like object in the :paramref:`file` argument supports the
        method ``write()`` to which the content should be written.

        :paramref:`text_is_expected` should be

        - :obj:`True` to pass a file to :paramref:`on_dump` that you can write
          strings to

        - :obj:`False` to pass a file to :paramref:`on_dump` that you can write
          bytes to
        """
        self.__dump_to_file = on_dump
        self.__text_is_expected = text_is_expected
        self.__encoding = encoding

    @property
    def encoding(self):
        """:return: the encoding for byte to string conversion
        :rtype: str"""
        return self.__encoding

    def string(self):
        """:return: the dump as a string"""
        if self.__text_is_expected:
            return self._string()
        else:
            return self._bytes().decode(self.__encoding)

    def _string(self):
        """:return: the string from a :class:`io.StringIO`"""
        file = StringIO()
        self.__dump_to_file(file)
        file.seek(0)
        return file.read()

    def bytes(self):
        """:return: the dump as bytes."""
        if self.__text_is_expected:
            return self.string().encode(self.__encoding)
        else:
            return self._bytes()

    def _bytes(self):
        """:return: bytes from a :class:`io.BytesIO`"""
        file = BytesIO()
        self.__dump_to_file(file)
        file.seek(0)
        return file.read()

    def file(self, file=None):
        """Saves the dump in a file-like object in text mode.

        :param file: :obj:`None` or a file-like object.
        :return: a file-like object

        If :paramref:`file` is :obj:`None`, a new :class:`io.StringIO`
        is returned.
        If :paramref:`file` is not :obj:`None` it should be a file-like object.

        The content is written to the file. After writing, the file's
        read/write position points behind the dumped content.
        """
        if file is None:
            file = StringIO()
        self._file(file)
        return file

    def _file(self, file):
        """Dump the content to a `file`.
        """
        if not self.__text_is_expected:
            file = BytesWrapper(file, self.__encoding)
        self.__dump_to_file(file)

    def binary_file(self, file=None):
        """Same as :meth:`file` but for binary content."""
        if file is None:
            file = BytesIO()
        self._binary_file(file)
        return file

    def _binary_file(self, file):
        """Dump the ocntent into the `file` in binary mode.
        """
        if self.__text_is_expected:
            file = TextWrapper(file, self.__encoding)
        self.__dump_to_file(file)

    def _mode_and_encoding_for_open(self):
        """:return: the file mode and encoding for :obj:`open`."""
        if self.__text_is_expected:
            return "w", self.__encoding
        return "wb", None

    def path(self, path):
        """Saves the dump in a file named :paramref:`path`.

        :param str path: a valid path to a file location. The file can exist.
        """
        self._path(path)

    def _path(self, path):
        """Saves the dump in a file named `path`."""
        mode, encoding = self._mode_and_encoding_for_open()
        with open(path, mode, encoding=encoding) as file:
            self.__dump_to_file(file)

    def _temporary_file(self, delete):
        """:return: a temporary file where the content is dumped to."""
        file = NamedTemporaryFile("w+", delete=delete,
                                  encoding=self.__encoding)
        self._file(file)
        return file

    def temporary_path(self, extension=""):
        """Saves the dump in a temporary file and returns its path.

        .. warning:: The user of this method is responsible for deleting this
                     file to save space on the hard drive.
                     If you only need a file object for a short period of time
                     you can use the method :meth:`temporary_file`.

        :param str extension: the ending ot the file name e.g. ``".png"``
        :return: a path to the temporary file
        :rtype: str
        """
        path = NamedTemporaryFile(delete=False, suffix=extension).name
        self.path(path)
        return path

    def temporary_file(self, delete_when_closed=True):
        """Saves the dump in a temporary file and returns the open file object.

        :param bool delete_when_closed: whether to delete the temporary file
                                        when it is closed.
        :return: a file-like object

        If :paramref:`delete_when_closed` is :obj:`True` (default) the file
        on the hard drive will be deleted if it is closed or not referenced
        any more.

        If :paramref:`delete_when_closed` is :obj:`False` the returned
        temporary file is not deleted when closed or unreferenced.
        The user of this method has then the responsibility to free the
        space on the host system.

        The returned file-like object has an attribute ``name`` that holds
        the location of the file.
        """
        return self._temporary_file(delete_when_closed)

    def binary_temporary_file(self, delete_when_closed=True):
        """Same as :meth:`temporary_file` but for binary mode."""
        return self._binary_temporary_file(delete_when_closed)
    temporary_binary_file = binary_temporary_file

    def _binary_temporary_file(self, delete):
        """:return: a binary temporary file where the content is dumped to."""
        file = NamedTemporaryFile("wb+", delete=delete)
        self._binary_file(file)
        return file

    def __repr__(self):
        """the string representation for people to read

        :return: the string represenation of this object
        :rtype: str
        """
        return "<{} in with encoding {} >".format(
                self.__class__.__name__,
                self.__encoding
            )


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
        from .ParsingSpecification import new_knitting_pattern_set_loader
        if specification is None:
            loader = new_knitting_pattern_set_loader()
        else:
            loader = new_knitting_pattern_set_loader(specification)
        return loader.object(self.object())


class XMLDumper(ContentDumper):
    """Used to dump objects as XML. Useful for dumping SVGs."""

    def __init__(self, on_dump):
        """Create a new XMLDumper object with the callable `on_dump`.

        `on_dump` takes no aguments and returns the object that should be
        serialized to XML."""
        super().__init__(self._dump_to_file)
        self.__dump_object = on_dump

    def object(self):
        """Return the object that should be dumped."""
        return self.__dump_object()

    def _dump_to_file(self, file):
        """dump to the file"""
        xmltodict.unparse(self.object(), file, pretty=True)


__all__ = ["ContentDumper", "JSONDumper", "XMLDumper"]
