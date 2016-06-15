
class BytesWrapper(object):

    def __init__(self, text_file, encoding):
        """Create a wrapper aroung `text_file` that decodes bytes to string
        using `encoding` and writes them to `text_file`"""
        self._file = text_file
        self._encoding = encoding

    def write(self, bytes):
        """Write bytes to the file."""
        string = bytes.decode(self._encoding)
        self._file.write(string)


class TextWrapper(object):

    def __init__(self, binary_file, encoding):
        """Create a wrapper aroung `binary_file` that encodes strings to bytes
        using `encoding` and writes them to `binary_file`"""
        self._file = binary_file
        self._encoding = encoding

    def write(self, string):
        """Write a string to the file."""
        bytes = string.encode(self._encoding)
        self._file.write(bytes)


__all__ = ["TextWrapper", "BytesWrapper"]
