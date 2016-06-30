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
    """The fucntion to call if a change happens."""
    def add_call(call):
        changes.append((call, call.elements[:]))
    return add_call


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
    """Calls an object s attribute and returns the result and the exception."""
    try:
        return getattr(obj, attr)(*args, **kw), None
    except:
        ty, err, tb = sys.exc_info()
        traceback.print_exception(ty, err, tb)
        return None, err


PRECONDITION = "Observable and real object should start as the same."
OBSERVER_IS_NOTIFIED = "The observer must be notified. "\
    "You probably forgot the call \"notifyObservers(change)\"."


class StepTester(object):
    
    def __init__(self, real, original, value, changes):
        self.real, self.observable = real
        self.real_original, self.observable_original = original
        self.value, self.observable_value = value
        self.changes_before, self.changes_after = changes
        self.assert_same()
    
    def assert_same(self):
        assert self.real_original == self.observable_original, PRECONDITION
        assert self.real == self.observable
        for i, element in enumerate(self.real):
            assert element == self.observable[i]
        assert all(a == b for a, b in zip(self.real, self.observable))
        assert len(self.real) == len(self.observable)
        real_is_same = self.real_original == self.real
        observable_is_same = self.observable == self.observable_original
        assert real_is_same == observable_is_same
        value, error = self.value
        observable_value, observable_error = self.observable_value
        assert value == observable_value
        assert error.__class__ == observable_error.__class__
        if error is not None:
            assert error.args == observable_error.args

    def assert_no_changes(self):
        assert self.changes_before == self.changes_after
        
    def assert_one_more_call(self):
        assert len(self.changes_before) == len(self.changes_after) - 1, \
            OBSERVER_IS_NOTIFIED
    
    def assert_add(self, index, elements):
        self.assert_one_more_call()
        self._assert_call(self.changes_after[-1], index, elements)
        for obj in (self.real, self.observable):
            self._assert_call_adds(obj, index, elements)
            
    def _assert_call(self, call_and_elements, index, elements, adds=True):
        call, call_elements = call_and_elements
        length = len(elements)
        assert call_elements == elements
        assert call.adds() == adds
        assert call.removes() != adds
        assert call.start == index
        assert call.stop == index + length
        assert call.length == length
        assert call.changed_object is self.observable
    
    def _assert_call_adds(self, obj, index, elements):
        for element in elements:
            assert element in obj
        for index, element in enumerate(elements, index):
            assert obj[index] == element
            assert obj.index(element) == index
        assert obj[index:index + len(elements)] == elements

    def assert_remove(self, index, elements):
        self.assert_one_more_call()
        self._assert_call(self.changes_after[-1], index, elements, adds=False)
    

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

class TestAddElements:

    def test_append_elements(self, chain):
        test = chain.append(3)
        test.assert_add(0, [3])
        
    def test_insert_element_at_end(self, chain):
        chain.insert(0, 224).assert_add(0, [224])

class TestRemoveElements:
    
    def _test_pop(chain):
        chain.extend([1, 2, 3, 4])
        chain.pop().assert_remove(3, [4])




