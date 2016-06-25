"""See this module if you like to store object s that have an ``id`` attribute.
"""
from collections import OrderedDict


class IdCollection(object):
    """This is a collections of object that have an ``id`` attribute."""

    def __init__(self):
        """Creat a new :class:`IdCollection` with no arguments.

        You can add objects later using the method :meth:`append`.
        """
        self._items = OrderedDict()

    def append(self, item):
        """Add an object to the end of the :class:`IdCollection`.

        :param item: an object that has an id
        """
        self._items[item.id] = item

    def at(self, index):
        """Get the object at an :paramref:`index`.

        :param int index: the index of the object
        :return: the object at :paramref:`index`
        """
        keys = list(self._items.keys())
        key = keys[index]
        return self[key]

    def __getitem__(self, id_):
        """Get the object with the :paramref:`id`

        .. code:: python

            ic = IdCollection()
            ic.append(object_1)
            ic.append(object_2)
            assert ic[object_1.id] == object_1
            assert ic[object_2.id] == object_1

        :param id_: the id of an object
        :return: the object with the :paramref:`id`
        :raises KeyError: if no object with :paramref:`id` was found
        """
        return self._items[id_]

    def __bool__(self):
        """:return: whether there is anything in the collection.
        :rtype: bool
        """
        return bool(self._items)

    def __iter__(self):
        """allows you to iterate and use for-loops

        The objects in the iterator have the order in which they were appended.
        """
        for id_ in self._items:
            yield self[id_]

    def __len__(self):
        """:return: the number of objects in this collection"""
        return len(self._items)
