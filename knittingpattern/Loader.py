import json
import os
import sys
from itertools import filterfalse


def indentity(object):
    """Returns the argument."""
    return object


def true(object):
    """Returns `True`."""
    return True


class PathLoader(object):
    """Load paths and folders from the local file system."""

    def __init__(self, process=indentity, chooses_path=true):
        """Create a PathLoader object.

        `process(path)` is called with the `path` to load as first argument.
        The result of process is returned to the caller.

        `chooses_path(path)` returns `True` or `False` depending on whether
        a specific path should be loaded"""
        self._process = process
        self._chooses_path = chooses_path

    def folder(self, folder):
        """Load all files from a folder recursively.

        Depending on `chooses_path` some paths will not be loaded.
        Every loaded path is processed and returned part of the returned list.
        """
        result = []
        for root, directories, files in os.walk(folder):
            for file in files:
                path = os.path.join(root, file)
                if self._chooses_path(path):
                    result.append(self.path(path))
        return result

    def chooses_path(self, path):
        """returns whether a `path` should be loaded."""
        return self._chooses_path(path)

    def path(self, path):
        """load a `path` and return the processed result."""
        return self._process(path)

    def _relative_to_absolute(self, module_location, folder):
        """Returns the absolute path for the `folder` relative to
        the module_location.

        `module_locetion` can be

        - a folder
        - a file
        - a module name
        """
        if os.path.isfile(module_location):
            path = os.path.dirname(module_location)
        elif os.path.isdir(module_location):
            path = module_location
        else:
            __import__(module_location)
            module = sys.modules[module_location]
            path = os.path.dirname(module.__file__)
        absolute_path = os.path.join(path, folder)
        return absolute_path

    def relative_folder(self, module, folder):
        """Load a folder located relative to a module and return the processed
        result.

        `module` can be

        - a folder
        - a file
        - a module name

        Depending on `chooses_path` some paths will not be loaded.
        Every loaded path is processed and returned part of the returned list.
        """
        folder = self._relative_to_absolute(module, folder)
        return self.folder(folder)

    def relative_file(self, module, file):
        """Load a file relative to a module.

        `module` can be

        - a folder
        - a file
        - a module name

        The processed result is returned.
        """
        path = self._relative_to_absolute(module, file)
        return self.path(path)

    def choose_paths(self, paths):
        """Returns a list of `paths` that are chosen by `chooses_path`."""
        return [path for path in paths if self._chooses_path(path)]


class ContentLoader(PathLoader):
    """Load contents of files and ressources."""

    def string(self, string):
        """returns the processed result of a string."""
        return self._process(string)

    def file(self, file):
        """Returns the processed result of the content of a file-like object.

        The file-like object should support the `read` method.
        """
        string = file.read()
        return self.string(string)

    def path(self, path):
        """Returns the processed result of a path's content.

        This path should exist on the local file system."""
        with open(path) as file:
            return self.file(file)

    def url(self, url, encoding="UTF-8"):
        """Load an process the content behind a url.

        The default `encoding` is UTF-8."""
        import urllib.request
        with urllib.request.urlopen(url) as file:
            webpage_content = file.read()
        webpage_content = webpage_content.decode(encoding)
        return self.string(webpage_content)


class JSONLoader(ContentLoader):
    """Load an process JSON from various locations."""

    def object(self, string):
        """Process an already loaded object."""
        return self._process(string)

    def string(self, string):
        """Load an object from a string and return the processes JSON content
        """
        object = json.loads(string)
        return self.object(object)


__all__ = ["JSONLoader", "ContentLoader", "PathLoader"]
