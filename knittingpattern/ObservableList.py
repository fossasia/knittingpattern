"""This module contains the ObservableList."""
from collections import UserList
from functools import wraps


class Change(object):

    def __init__(self, list_, index, length):
        """Initialize the change.
        
        :param list list_: the list that changed
        :param int index: the place where the change took place
        :param int length: the length of the change
        """
        self._list = list_
        self._length = length
        self._index = self._prepare_index(index)
    
    def _prepare_index(self, index):
        """Adjust the index."""
        length = len(self._list)
        max_index = length - 1
        if index > max_index:
            return max_index
        if index < 0:
            return length + index
        return index
    
    @property
    def elements(self):
        """The elements affected by this change.
        
        :rtype: list
        """
        return self._list[self._index:self._index + self._length]
    
    @property
    def start(self):
        """The start index of the change.
        
        :rtype: int
        """
        return self._index
    
    @property
    def stop(self):
        """The stop index of the change.
        
        :rtype: int
        
        .. note:: As with lists, the element at the stop index is excluded
          from the change.
        """
        return self._index + self._length
    
    @property
    def length(self):
        """The number of elements changed.
        
        :rtype: int
        """
        return self._length
    
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
        return "<{} {}[{}:{}]>".format(
                self.__class__.__name__,
                self.changed_object,
                self.start,
                self.stop
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
    
    def __init__(self):
        self.observers = []

    def registerObserver(self, observer):
        """Register an observer.
        
        :param observer: callable that takes a :class:`Change` as first
          argument
        """
        self.observers.append(observer)
        
    def notifyObservers(self, change):
        """Notify the observers about the change."""
        print(change)
        for observer in self.observers:
            observer(change)
        
    def _notify_add(self, index, length):
        """Notify about an AddChange."""
        change = AddChange(self, index, length)
        self.notifyObservers(change)
    
    def _notify_remove(self, index, length):
        """Notify about a RemoveChange."""
        change = RemoveChange(self, index, length)
        self.notifyObservers(change)
    
    def append(self, element):
        index = len(self)
        super().append(element)
        self._notify_add(index, 1)
    
    def insert(self, index, *args):
        super().insert(index, *args)
        if index < 0:
            index -= 1
        self._notify_add(index, 1)
    
    def extend(self, other):
        index = len(self)
        length = 0
        for length, element in enumerate(other, 1):
            super().append(element)
        if length:
            self._notify_add(index, length)
    
    def pop(self, index=-1):
        self._notify_remove(index, 1)
        return super().pop(index)

    def remove(self, element):
        try:
            index = self.index(element)
        except ValueError:
            raise ValueError("list.remove(x): x not in list")
        else:
            self._notify_remove(index, 1)
            super().pop(index)
    
    def clear(self):
        length = len(self)
        if length:
            self._notify_remove(0, length)
        super().clear()




