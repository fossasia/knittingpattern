"""This module contains the ObservableList."""
from collections import UserList
from functools import wraps


class Change(object):

    def __init__(self, list_, slice_):
        """Initialize the change.

        :param list list_: the list that changed
        :param slice slice_: the slice of the :paramref:`list_` to change
        """
        self._slice = slice_
        self._list = list_
        self._start, self._stop, self._step = self._slice.indices(len(list_))

    @property
    def elements(self):
        """The elements affected by this change.

        :rtype: list
        """
        return self._list[self._slice]

    @property
    def start(self):
        """The start index of the change.

        :rtype: int
        """
        return self._start

    @property
    def stop(self):
        """The stop index of the change.

        :rtype: int

        .. note:: As with lists, the element at the stop index is excluded
          from the change.
        """
        return self._stop

    @property
    def step(self):
        """The step size of the change.

        :rtype: int
        """
        return self._step

    @property
    def length(self):
        """The number of elements changed.

        :rtype: int

        .. code:: python

            assert change.length == len(change.indices)
            assert change.length == len(change.elements)
        """
        span = self._stop - self._start
        length, modulo = divmod(span, self._step)
        if length < 0:
            return 0
        if modulo != 0:
            return length + 1
        return length

    @property
    def range(self):
        """The indices of the changed objects.

        :rtype: range
        """
        return range(self._start, self._stop, self._step)

    @property
    def changed_object(self):
        """The object that was changed.

        :return: the object that was changed
        """
        return self._list

    def adds(self):
        """Whether the change adds values.

        :rtype: bool
        """
        return False

    def removes(self):
        """Whether the change removes values.

        :rtype: bool
        """
        return False

    def __repr__(self):
        """The change as string."""
        step = ":{}".format(self.step) if self.step != 1 else ""
        return "<{} {}[{}:{}{}]>".format(
                self.__class__.__name__,
                self.changed_object,
                self.start,
                self.stop,
                step
            )


class AddChange(Change):

    def adds(self):
        """This change adds values.

        :rtype: bool
        :return: :obj:`True`
        """
        return True


class RemoveChange(Change):

    def removes(self):
        """This change removes values.

        :rtype: bool
        :return: :obj:`True`
        """
        return True


class ObservableList(list):

    """The observable list behaves like a list but changees can be observed.

    See the `Observer Pattern
    <https://en.wikipedia.org/wiki/Observer_pattern>`__ for more understanding.

    """

    @wraps(list.__init__)
    def __init__(self):
        self._observers = []

    def registerObserver(self, observer):
        """Register an observer.

        :param observer: callable that takes a :class:`Change` as first
          argument
        """
        self._observers.append(observer)

    def notifyObservers(self, change):
        """Notify the observers about the change."""
        print(change)
        for observer in self._observers:
            observer(change)

    def _notify_add(self, slice_):
        """Notify about an AddChange."""
        change = AddChange(self, slice_)
        self.notifyObservers(change)

    def _notify_add_at(self, index, length=1):
        slice_ = self._slice_at(index, length)
        self._notify_add(slice_)

    def _notify_remove_at(self, index, length=1):
        slice_ = self._slice_at(index, length)
        self._notify_remove(slice_)

    def _notify_remove(self, slice_):
        """Notify about a RemoveChange."""
        change = RemoveChange(self, slice_)
        self.notifyObservers(change)

    def _slice_at(self, index, length=1):
        print("slice at {}, {}".format(index, length))
        length_ = len(self)
        if -length <= index < 0:
            index += length_
        return slice(index, index + length)

    @wraps(list.append)
    def append(self, element):
        super().append(element)
        self._notify_add_at(len(self) - 1)

    @wraps(list.insert)
    def insert(self, index, item):
        super().insert(index, item)
        length = len(self)
        if index >= length:
            index = length - 1
        elif index < 0:
            index += length - 1
            if index < 0:
                index = 0
        self._notify_add_at(index)

    @wraps(list.extend)
    def extend(self, other):
        index = len(self)
        length = 0
        for length, element in enumerate(other, 1):
            super().append(element)
        if length:
            self._notify_add_at(index, length)

    @wraps(list.__iadd__)
    def __iadd__(self, other):
        self.extend(other)
        return self

    @wraps(list.__imul__)
    def __imul__(self, multiplier):
        if not isinstance(multiplier, int):
            return super().__imul__(multiplier)
        length = len(self)
        if not length or multiplier == 1:
            return self
        if multiplier <= 0:
            self._notify_remove_at(0, length)
        super().__imul__(multiplier)
        new_length = len(self)
        if new_length:
            self._notify_add(slice(length, new_length))
        return self

    @wraps(list.pop)
    def pop(self, index=-1):
        if not isinstance(index, int):
            raise TypeError("'str' object cannot be interpreted as an integer")
        length = len(self)
        if -length <= index < length:
            self._notify_remove_at(index)
        return super().pop(index)

    @wraps(list.remove)
    def remove(self, element):
        try:
            index = self.index(element)
        except ValueError:
            raise ValueError("list.remove(x): x not in list")
        else:
            self._notify_remove_at(index)
            super().pop(index)

    @wraps(list.clear)
    def clear(self):
        length = len(self)
        if length:
            self._notify_remove_at(0, length)
        super().clear()

    @wraps(list.__delitem__)
    def __delitem__(self, index_or_slice):
        self._notify_delete(index_or_slice)
        super().__delitem__(index_or_slice)

    @wraps(list.__setitem__)
    def __setitem__(self, index_or_slice, value):
        notify_add = self._notify_delete(index_or_slice)
        super().__setitem__(index_or_slice, value)
        notify_add()

    def _notify_delete(self, index_or_slice):
        if isinstance(index_or_slice, int):
            length = len(self)
            if -length <= index_or_slice < length:
                self._notify_remove_at(index_or_slice)
                return lambda: self._notify_add_at(index_or_slice)
        elif isinstance(index_or_slice, slice):
            slice_ = slice(*index_or_slice.indices(len(self)))
            self._notify_remove(slice_)
            return lambda: self._notify_add(index_or_slice)

__all__ = ["ObservableList", "Change", "AddChange", "RemoveChange"]
