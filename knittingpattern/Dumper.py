"""Writing objects to files

This module offers a unified interface to serialize objects to strings
and save them to files.
"""
from io import StringIO, BytesIO
from tempfile import NamedTemporaryFile
import json
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
        """Create a new dumper object with a function `on_dump(file)`

        The dumper calls `on_dump(file)` with a file-like object every time
        one of its save methods, `string`, `file`, ..., is called.
        The file-like object in the 'file' argument supports the method
        `write` to which the content should be written.

        `text_is_expected` should be
        - `True` to pass a file to `on_dump` that you can write strings to
        - `False` to pass a file to `on_dump` that you can write bytes to

        """
        self.__dump_to_file = on_dump
        self.__text_is_expected = text_is_expected
        self.__encoding = encoding

    @property
    def encoding(self):
        """return the encoding for byte to string conversion."""
        return self.__encoding

    def string(self):
        """Returns the dump as a string."""
        if self.__text_is_expected:
            return self._string()
        else:
            return self._bytes().decode(self.__encoding)

    def _string(self):
        """Return the string from a StringIO()"""
        file = StringIO()
        self.__dump_to_file(file)
        file.seek(0)
        return file.read()

    def bytes(self):
        """Returns the dump as bytes."""
        if self.__text_is_expected:
            return self.string().encode(self.__encoding)
        else:
            return self._bytes()

    def _bytes(self):
        """Returns bytes from a BytesIO()"""
        file = BytesIO()
        self.__dump_to_file(file)
        file.seek(0)
        return file.read()

    def file(self, file=None):
        """Saves the dump in a file-like object in text mode.

        If `file` is `None`, a new file-like object(StringIO) is returned.

        If `file` is not `None` it should be a file-like object.
        The content is written to the file. After writing, the file's
        read/write position points behind the dumped content.
        """
        if file is None:
            file = StringIO()
        self._file(file)
        return file

    def _file(self, file):
        """Dump the content to a `file`.

        `instead` is the method that should be used if encoding does not work.
        """
        if not self.__text_is_expected:
            file = BytesWrapper(file, self.__encoding)
        self.__dump_to_file(file)

    def binary_file(self, file=None):
        """Same as `file()` but for binary content."""
        if file is None:
            file = BytesIO()
        self._binary_file(file)
        return file

    def _binary_file(self, file):
        """Dump the ocntent into the `file` in binary mode.

        `instead` is the method that should be used if encoding does not work.
        """
        if self.__text_is_expected:
            file = TextWrapper(file, self.__encoding)
        self.__dump_to_file(file)

    def _mode_and_encoding_for_open(self):
        """Returns the file mode and encoding for `open()`."""
        if self.__text_is_expected:
            return "w", self.__encoding
        return "wb", None

    def path(self, path):
        """Saves the dump in a file named `path`."""
        self._path(path)

    def _path(self, path):
        """Saves the dump in a file named `path`."""
        mode, encoding = self._mode_and_encoding_for_open()
        with open(path, mode, encoding=encoding) as file:
            self.__dump_to_file(file)

    def _temporary_file(self, delete):
        """Returns a temporary file where the content is dumped to."""
        file = NamedTemporaryFile("w+", delete=delete,
                                  encoding=self.__encoding)
        self._file(file)
        return file

    def temporary_path(self, extension=""):
        """Saves the dump in a temporary file and returns its path.

        The user of this method is responsible for deleting this file to
        save space on the hard drive. If you only need a file object for
        a short period of time you can use the method `temporary_file()`.

        `extension` is the ending ot the file name e.g. ".png".
        """
        path = NamedTemporaryFile(delete=False, suffix=extension).name
        self.path(path)
        return path

    def temporary_file(self, delete_when_closed=True):
        """Saves the dump in a temporary file and returns the open file object.

        If `delete_when_closed` is `True` (default) the file on the hard drive
        will be deleted if it is closed or not referenced any more.

        If `delete_when_closed` is `False` the returned temporary file is not
        deleted when closed or unreferenced.
        The user of this method has then the responsibility to free the
        system space.

        The returned file-like object has an attribute `name` that holds
        the location of the file.
        """
        return self._temporary_file(delete_when_closed)

    def binary_temporary_file(self, delete_when_closed=True):
        """Same as `temporary_file` but for binary mode."""
        return self._binary_temporary_file(delete_when_closed)
    temporary_binary_file = binary_temporary_file

    def _binary_temporary_file(self, delete):
        """Returns a binary temporary file where the content is dumped to."""
        file = NamedTemporaryFile("wb+", delete=delete)
        self._binary_file(file)
        return file

    def __repr__(self):
        """Return the string represenation of this object."""
        name = getattr(self.__dump_to_file, "__name__", self.__dump_to_file)
        mode = ("text" if self.__text_is_expected else "bytes")
        return "<{} for {} in {} mode encoded in {} >".format(
                self.__class__.__name__,
                name,
                mode,
                self.__encoding
            )


class JSONDumper(ContentDumper):

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


__all__ = ["ContentDumper"]
