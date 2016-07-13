"""One can load objects from different locations.
This module provides functionality to load objects from different locations
while preserving a simple interface to the cosumer.

"""
import json
import os
import sys


def identity(object_):
    """:return: the argument
    :param object_: the object to be returned"""
    return object_


def true(_):
    """:return: :obj:`True`
    :param _: can be ignored"""
    return True


class PathLoader(object):
    """Load paths and folders from the local file system.

    The :paramref:`process <PathLoader.__init__.process>` is called with a
    :class:`path <str>` as first argument: ``process(path)``.
    """

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
        for root, _, files in os.walk(folder):
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
            module_folder = os.path.dirname(module_location)
            if module_folder:
                path = module_folder
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

    def example(self, relative_path):
        """Load an example from the knitting pattern examples.

        :param str relative_path: the path to load
        :return: the result of the processing

        You can use :meth:`knittingpattern.Loader.PathLoader.examples`
        to find out the paths of all examples.
        """
        example_path = os.path.join("examples", relative_path)
        return self.relative_file(__file__, example_path)

    def examples(self):
        """Load all examples form the examples folder of this packge.

        :return: a list of processed examples
        :rtype: list

        Depending on :meth:`chooses_path` some paths may not be loaded.
        Every loaded path is processed and returned part of the returned list.
        """
        return self.relative_folder(__file__, "examples")


class ContentLoader(PathLoader):
    """Load contents of files and ressources.

    The :paramref:`process <PathLoader.__init__.process>` is called with a
    :class:`string <str>` as first argument: ``process(string)``.
    """

    def string(self, string):
        """:return: the processed result of a string
        :param str string: the string to load the ocntent from
        """
        return self._process(string)

    def file(self, file):
        """:return: the processed result of the content of a file-like object.

        :param file: the file-like object to load the content from.
          It should support the ``read`` method.
        """
        string = file.read()
        return self.string(string)

    def path(self, path):
        """:return: the processed result of a :paramref:`path's <path>` content.
        :param str path: the path where to load the content from.
          It should exist on the local file system.
        """
        with open(path) as file:
            return self.file(file)

    def url(self, url, encoding="UTF-8"):
        """load and process the content behind a url

        :return: the processed result of the :paramref:`url's <url>` content
        :param str url: the url to retrieve the content from
        :param str encoding: the encoding of the retrieved content.
          The default encoding is UTF-8.

        """
        import urllib.request
        with urllib.request.urlopen(url) as file:
            webpage_content = file.read()
        webpage_content = webpage_content.decode(encoding)
        return self.string(webpage_content)


class JSONLoader(ContentLoader):
    """Load an process JSON from various locations.

    The :paramref:`process <PathLoader.__init__.process>` is called with an
    :class:`object` as first argument: ``process(object)``.
    """

    def object(self, object_):
        """Processes an already loaded object.

        :return: the result of the processing step
        :param object: the object to be loaded
        """
        return self._process(object_)

    def string(self, string):
        """Load an object from a string and return the processed JSON content

        :return: the result of the processing step
        :param str string: the string to load the JSON from
        """
        object_ = json.loads(string)
        return self.object(object_)


__all__ = ["JSONLoader", "ContentLoader", "PathLoader", "true", "identity"]
