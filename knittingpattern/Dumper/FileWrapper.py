"""This module provides wrappers for file-like objects
for encoding and decoding.

"""


class BytesWrapper(object):
    """Use this class if you have a text-file but you want to
    write bytes to it.
    """

    def __init__(self, text_file, encoding):
        """Create a wrapper around :paramref:`text_file` that decodes
        bytes to string using :paramref:`encoding` and writes them
        to :paramref:`text_file`.

        :param str encoding: The encoding to use to transfer the written bytes
          to string so they can be written to :paramref:`text_file`
        :param text_file: a file-like object open in text mode
        """
        self._file = text_file
        self._encoding = encoding

    def write(self, bytes_):
        """Write bytes to the file."""
        string = bytes_.decode(self._encoding)
        self._file.write(string)


class TextWrapper(object):
    """Use this class if you have a binary-file but you want to
    write strings to it.
    """

    def __init__(self, binary_file, encoding):
        """Create a wrapper around :paramref:`binary_file` that encodes
        strings to bytes using :paramref:`encoding` and writes them
        to :paramref:`binary_file`.

        :param str encoding: The encoding to use to transfer the written string
          to bytes so they can be written to :paramref:`binary_file`
        :param binary_file: a file-like object open in binary mode
        """
        self._file = binary_file
        self._encoding = encoding

    def write(self, string):
        """Write a string to the file."""
        bytes_ = string.encode(self._encoding)
        self._file.write(bytes_)


__all__ = ["TextWrapper", "BytesWrapper"]
