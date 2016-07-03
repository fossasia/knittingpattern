"""This module contains the ObservableList."""


class Change(object):

    """The base class for changes."""

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

    def items(self):
        """Return an iterable over pairs of index and value."""
        return zip(self.range, self.elements)


class AddChange(Change):

    """A change that adds elements."""

    def adds(self):
        """Whether the change adds values (True).

        :rtype: bool
        :return: :obj:`True`
        """
        return True


class RemoveChange(Change):

    """A change that removes elements."""

    def removes(self):
        """Whether the change removes values (True).

        :rtype: bool
        :return: :obj:`True`
        """
        return True


class ObservableList(list):

    """The observable list behaves like a list but changes can be observed.

    See the `Observer Pattern
    <https://en.wikipedia.org/wiki/Observer_pattern>`__ for more understanding.

    """

    def __init__(self, iterable=()):
        """See :class:`list`."""
        self._observers = []
        self.extend(iterable)

    def register_observer(self, observer):
        """Register an observer.

        :param observer: callable that takes a :class:`Change` as first
          argument
        """
        self._observers.append(observer)

    def notify_observers(self, change):
        """Notify the observers about the change."""
        for observer in self._observers:
            observer(change)

    def _notify_add(self, slice_):
        """Notify about an AddChange."""
        change = AddChange(self, slice_)
        self.notify_observers(change)

    def _notify_add_at(self, index, length=1):
        """Notify about an AddChange at a caertain index and length."""
        slice_ = self._slice_at(index, length)
        self._notify_add(slice_)

    def _notify_remove_at(self, index, length=1):
        """Notify about an RemoveChange at a caertain index and length."""
        slice_ = self._slice_at(index, length)
        self._notify_remove(slice_)

    def _notify_remove(self, slice_):
        """Notify about a RemoveChange."""
        change = RemoveChange(self, slice_)
        self.notify_observers(change)

    def _slice_at(self, index, length=1):
        """Create a slice for index and length."""
        length_ = len(self)
        if -length <= index < 0:
            index += length_
        return slice(index, index + length)

    def append(self, element):
        """See list.append."""
        super().append(element)
        self._notify_add_at(len(self) - 1)

    def insert(self, index, item):
        """See list.insert."""
        super().insert(index, item)
        length = len(self)
        if index >= length:
            index = length - 1
        elif index < 0:
            index += length - 1
            if index < 0:
                index = 0
        self._notify_add_at(index)

    def extend(self, other):
        """See list.extend."""
        index = len(self)
        length = 0
        for length, element in enumerate(other, 1):
            super().append(element)
        if length:
            self._notify_add_at(index, length)

    def __iadd__(self, other):
        """See list.__iadd__."""
        self.extend(other)
        return self

    def __imul__(self, multiplier):
        """See list.__imul__."""
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

    def pop(self, index=-1):
        """See list.pop."""
        if not isinstance(index, int):
            raise TypeError("'str' object cannot be interpreted as an integer")
        length = len(self)
        if -length <= index < length:
            self._notify_remove_at(index)
        return super().pop(index)

    def remove(self, element):
        """See list.remove."""
        try:
            index = self.index(element)
        except ValueError:
            raise ValueError("list.remove(x): x not in list")
        else:
            self._notify_remove_at(index)
            super().pop(index)

    def clear(self):
        """See list.clear."""
        length = len(self)
        if length:
            self._notify_remove_at(0, length)
        super().clear()

    def __delitem__(self, index_or_slice):
        """See list.__delitem__."""
        self._notify_delete(index_or_slice)
        super().__delitem__(index_or_slice)

    def __setitem__(self, index_or_slice, value):
        """See list.__setitem__."""
        notify_add = self._notify_delete(index_or_slice)
        super().__setitem__(index_or_slice, value)
        notify_add()

    def _notify_delete(self, index_or_slice):
        """Notify about a deletion at an index_or_slice.

        :return: a function that notifies about an add at the same place.
        """
        if isinstance(index_or_slice, int):
            length = len(self)
            if -length <= index_or_slice < length:
                self._notify_remove_at(index_or_slice)
                return lambda: self._notify_add_at(index_or_slice)
        elif isinstance(index_or_slice, slice):
            slice_ = slice(*index_or_slice.indices(len(self)))
            self._notify_remove(slice_)
            return lambda: self._notify_add(index_or_slice)

#: The methods that are replaced in :class:`ObservableList`.
REPLACED_METHODS = ["__setitem__", "__delitem__", "clear", "remove", "pop",
                    "__imul__", "insert", "append", "extend", "__iadd__",
                    "__init__"]

for method_name in REPLACED_METHODS:
    method = getattr(ObservableList, method_name)
    method.__doc__ = getattr(list, method_name).__doc__
del method, method_name

__all__ = ["ObservableList", "Change", "AddChange", "RemoveChange"]
