"""Test the observable list.

The :class:`knittingpattern.ObservableList.ObservableList` is a 
:class:`list` implementing the observer pattern.
This way, a row can be notifies abot the change in its instructions.
"""

from test_knittingpattern import fixture, MagicMock
from knittingpattern.ObservableList import ObservableList
from weakref import WeakKeyDictionary
from functools import wraps
import sys
import traceback


@fixture
def changes():
    """A list of changes made."""
    return []


@fixture
def onchange(changes):
    """The fucntion to change if a change happens."""
    def add_change(change):
        changes.append((change, change.elements[:]))
    return add_change


@fixture
def ol(onchange):
    """The observable list."""
    ol_ = ObservableList()
    ol_.registerObserver(onchange)
    return ol_



class OtherSelf(object):
    
    """Class for other selves."""


other_selves = WeakKeyDictionary()

def other_self(func):
    """Wrapper for functions that prefer an other self."""
    @wraps(func)
    def wrapper(self, *args, **kw):
        other_self = other_selves.get(self, OtherSelf())
        other_selves.setdefault(self, other_self)
        return func(other_self, *args, **kw)
    return wrapper


def call_attr(obj, attr, args, kw):
    """Calls an object s attribute and returns the result and the exception.
    
    :param obj: the object to call the method on
    :param: attr: the attribute to get the coallable from
    :param tuple args: a tuple of arguments. If elements of :paramref:`args`
      are callable, their evaluation result becones the argument. This is
      useful if you pass a mutable object i.e. a generator.
    :param dict kw: the keyword arguments
    """
    args_ = []
    for arg in args:
        if callable(arg):
            args_.append(arg())
        else:
            args_.append(arg)
    try:
        return getattr(obj, attr)(*args_, **kw), None
    except:
        ty, err, tb = sys.exc_info()
        traceback.print_exception(ty, err, tb)
        return None, err


PRECONDITION = "Observable and real object should start as the same."
OBSERVER_IS_NOTIFIED = "The observer must be notified. "\
    "You probably forgot the call \"notifyObservers(change)\"."
ERROR_SAME = "error is the same"

class StepTester(object):
    
    def __init__(self, real, original, value, changes):
        self.real, self.observable = real
        self.real_original, self.observable_original = original
        self.value, self.observable_value = value
        self.changes_before, self.changes_after = changes
        self.assert_same()
    
    def assert_same(self):
        assert self.real_original == self.observable_original, PRECONDITION
        print("real: {} observable: {}".format(self.real, self.observable))
        assert self.real == self.observable
        for i, element in enumerate(self.real):
            assert element == self.observable[i]
        assert all(a == b for a, b in zip(self.real, self.observable))
        assert len(self.real) == len(self.observable)
        for element in self.real:
            assert self.real.count(element) == self.observable.count(element)
        real_is_same = self.real_original == self.real
        observable_is_same = self.observable == self.observable_original
        assert real_is_same == observable_is_same
        value, error = self.value
        observable_value, observable_error = self.observable_value
        assert value == observable_value, "return values are the same"
        assert error.__class__ == observable_error.__class__, ERROR_SAME
        if error is not None:
            assert error.args == observable_error.args, ERROR_SAME

    def assert_no_change(self):
        assert self.changes_before == self.changes_after
        
    def assert_one_more_change(self):
        assert len(self.changes_before) == len(self.changes_after) - 1, \
            OBSERVER_IS_NOTIFIED
    
    def assert_add(self, index, elements):
        self.assert_one_more_change()
        self._assert_change(self.changes_after[-1], index, elements)
        for obj in (self.real, self.observable):
            self._assert_change_adds(obj, index, elements)
            
    def _assert_change(self, change_and_elements, index, elements, adds=True):
        change, change_elements = change_and_elements
        length = len(elements)
        assert change.adds() == adds
        assert change.removes() != adds
        assert change.start == index
        assert change.stop == index + length
        assert change.length == length
        assert change.changed_object is self.observable
        assert change_elements == elements
    
    def _assert_change_adds(self, obj, index, elements):
        for element in elements:
            assert element in obj
        for i, element in enumerate(elements, index):
            assert obj[i] == element
            assert obj.index(element) == i
        assert obj[index:index + len(elements)] == elements

    def assert_remove(self, index, elements):
        self.assert_one_more_change()
        self._assert_change(self.changes_after[-1], index, elements, adds=False)
    

class ObservableChain(object):
    
    @other_self
    def __init__(self, real_list, observable_list, changes):
        self.real_list = real_list
        self.observable_list = observable_list
        self.changes = changes
    
    @other_self
    def __getattribute__(self, attr):
        if hasattr(self, attr):
            return getattr(self, attr)
        def call(*args, **kw):
            original_list = self.real_list[:]
            original_observable_list = self.observable_list[:]
            original_changes = self.changes[:]
            observable_value = call_attr(self.observable_list, attr, args, kw)
            real_value = call_attr(self.real_list, attr, args, kw)
            return StepTester((self.real_list, self.observable_list),
                              (original_list, original_observable_list),
                              (real_value, observable_value), 
                              (original_changes, self.changes))
        return call


@fixture
def chain(ol, changes):
    return ObservableChain([], ol, changes)

class TestInitialization:

    def test_empty_list_makes_no_changes(self, ol, changes):
        assert changes == []

    def test_empty_list_does_not_contain_anything(self, ol):
        for i in range(10):
            assert i not in ol

class TestObserver:

    def test_notify_observers_mock(self, ol):
        observer = MagicMock()
        change = MagicMock()
        ol.registerObserver(observer)
        ol.notifyObservers(change)
        observer.assert_called_with(change)

    def test_notify_observers(self, ol, changes):
        change = MagicMock()
        ol.notifyObservers(change)
        assert len(changes) == 1
        assert changes[0][0] is change


# To test:
# def __init__(self, initlist=None):
# def __repr__(self):
# def __lt__(self, other): 
# def __le__(self, other):
# def __eq__(self, other):
# def __gt__(self, other): 
# def __ge__(self, other): 
# def __contains__(self, item): 
# def __len__(self): 
# def __getitem__(self, i):
# def __setitem__(self, i, item):  
# def __delitem__(self, i): 
# def __add__(self, other):
# def __radd__(self, other):
# def __iadd__(self, other):
# def __mul__(self, n):
# __rmul__ = __mul__
# def __imul__(self, n):
# def append(self, item):          tested in TestAddElements
# def insert(self, i, item):       tested in TestAddElements
# def pop(self, i=-1):             tested in TestRemoveElements
# def remove(self, item):          tested in TestRemoveElements
# def clear(self):                 tested in TestRemoveElements
# def copy(self): 
# def count(self, item):           tested StepTester
# def index(self, item, *args):    tested StepTester
# def reverse(self):
# def sort(self, *args, **kwds):
# def extend(self, other):         tested in TestAddElements



class TestAddElements:

    def test_append_elements(self, chain):
        chain.append(3).assert_add(0, [3])
        chain.append(99).assert_add(1, [99])
        
    def test_insert_element_at_end(self, chain):
        chain.insert(0, 224).assert_add(0, [224])
        chain.insert(2, 223).assert_add(1, [223])
        chain.insert(-2, 222).assert_add(0, [222])
    
    def test_extend(self, chain):
        chain.extend([9, 8, 7, 6]).assert_add(0, [9, 8, 7, 6])
        chain.extend(lambda:(str(i) for i in range(3))).assert_add(4, ["0", "1", "2"])
        chain.extend([]).assert_no_change()



class TestRemoveElements:
    
    def test_pop(self, chain):
        chain.extend([1, 2, 3, 4])
        chain.pop().assert_remove(3, [4])
    
    def test_remove(self, chain):
        chain.extend(range(30))
        chain.remove(10).assert_remove(10, [10])
        chain.remove(10).assert_no_change()

    def test_clear(self, chain):
        chain.clear().assert_no_change()
        chain.extend([1, 2, 3, 4])
        chain.clear().assert_remove(0, [1, 2, 3, 4])
        chain.clear().assert_no_change()
