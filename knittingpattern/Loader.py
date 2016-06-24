"""One can load objects from different locations. 
This module provides functionality to load objects from different locations
while preserving a simple interface to the cosumer.

"""
import json
import os
import sys
from itertools import filterfalse


def identity(object):
    """:return: the argument
    :param object: the object to be returned"""
    return object


def true(object):
    """:return: :obj:`True`
    :param object: can be ignored"""
    return True


class PathLoader(object):
    """Load paths and folders from the local file system."""

    def __init__(self, process=identity, chooses_path=true):
        """Create a PathLoader object.

        :param process: ``process(path)`` is called with the `path` to load.
          The result of :paramref:`process` is returned to the caller. The
          default value is :func:`identity`, so the paths are returned when
          loaded.
        :param chooses_path: ``chooses_path(path)`` is called before
          :paramref:`process` and returns :obj:`True` or :obj:`False`
          depending on whether a specific path should be loaded and passed to
          :paramref:`process`.
        """
        self._process = process
        self._chooses_path = chooses_path

    def folder(self, folder):
        """Load all files from a folder recursively.

        Depending on :meth:`chooses_path` some paths may not be loaded.
        Every loaded path is processed and returned part of the returned list.
        
        :param str folder: the folder to load the files from
        :rtype: list
        :return: a list of the results of the processing steps of the loaded
          files
        """
        result = []
        for root, directories, files in os.walk(folder):
            for file in files:
                path = os.path.join(root, file)
                if self._chooses_path(path):
                    result.append(self.path(path))
        return result

    def chooses_path(self, path):
        """:return: whether the path should be loaded
        :rtype: bool
        
        :param str path: the path to the file to be tested
        """
        return self._chooses_path(path)

    def path(self, path):
        """load a :paramref:`path` and return the processed result
        
        :param str path: the path to the file to be processed
        :return: the result of processing step
        """
        return self._process(path)

    def _relative_to_absolute(self, module_location, folder):
        """:return: the absolute path for the `folder` relative to
        the module_location.
        :rtype: str
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

        :param str module: can be
        
          - a path to a folder
          - a path to a file
          - a module name
        
        :param str folder: the path of a folder relative to :paramref:`module`
        :return: a list of the results of the processing
        :rtype: list

        Depending on :meth:`chooses_path` some paths may not be loaded.
        Every loaded path is processed and returned part of the returned list.
        You can use :meth:`choose_paths` to find out which paths are chosen to
        load.
        """
        folder = self._relative_to_absolute(module, folder)
        return self.folder(folder)

    def relative_file(self, module, file):
        """Load a file relative to a module.

        :param str module: can be
        
          - a path to a folder
          - a path to a file
          - a module name
        
        :param str folder: the path of a folder relative to :paramref:`module`
        :return: the result of the processing
        
        """
        path = self._relative_to_absolute(module, file)
        return self.path(path)

    def choose_paths(self, paths):
        """:return: the paths that are chosen by :meth:`chooses_path`
        :rtype: list
        """
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


__all__ = ["JSONLoader", "ContentLoader", "PathLoader", "true", "identity"]
