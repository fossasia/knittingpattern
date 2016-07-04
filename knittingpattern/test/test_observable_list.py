"""Test the observable list.

The :class:`knittingpattern.ObservableList.ObservableList` is a
:class:`list` implementing the observer pattern.
This way, a row can be notifies abot the change in its instructions.
"""

from test_knittingpattern import fixture, MagicMock, pytest
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
    ol_.register_observer(onchange)
    return ol_


class OtherSelf(object):

    """Class for other selves."""

    def call(self, attr):
        def call(*args, **kw):
            before_list = self.real_list[:]
            before_observable_list = self.observable_list[:]
            before_changes = self.changes[:]
            observable_value = call_attr(self.observable_list, attr, args, kw)
            real_value = call_attr(self.real_list, attr, args, kw)
            return StepTester((self.real_list, self.observable_list),
                              (before_list, before_observable_list),
                              (real_value, observable_value),
                              (before_changes, self.changes))
        return call

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
    "You probably forgot the call \"notify_observers(change)\"."
ERROR_SAME = "error is the same"


class StepTester(object):

    def __init__(self, real, before, value, changes):
        self.real, self.observable = real
        self.real_before, self.observable_before = before
        self.value, self.observable_value = value
        self.changes_before, self.changes_after = changes
        self.assert_same()

    def assert_same(self):
        assert self.real_before == self.observable_before, PRECONDITION
        assert self.real == self.observable
        for i, element in enumerate(self.real):
            assert element == self.observable[i]
        assert all(a == b for a, b in zip(self.real, self.observable))
        assert len(self.real) == len(self.observable)
        for element in self.real:
            assert self.real.count(element) == self.observable.count(element)
        real_is_same = self.real_before == self.real
        observable_is_same = self.observable == self.observable_before
        assert real_is_same == observable_is_same
        value, error = self.value
        observable_value, observable_error = self.observable_value
        assert value == observable_value, "return values are the same"
        assert error.__class__ == observable_error.__class__, ERROR_SAME
        if error is not None:
            assert error.args == observable_error.args, ERROR_SAME
        real_is_same = self.real_before is self.real
        observable_is_same = self.observable_before is self.observable
        assert real_is_same == observable_is_same, "identity of result is same"

    def assert_no_change(self):
        assert self.changes_before == self.changes_after

    def assert_one_more_change(self, changes=1):
        assert len(self.changes_before) == len(self.changes_after) - changes, \
            OBSERVER_IS_NOTIFIED

    def assert_add(self, index, elements):
        self.assert_one_more_change()
        self._assert_add(index, elements)

    def _assert_add(self, index, elements):
        self._assert_change(self.changes_after[-1], index, elements)
        for obj in (self.real, self.observable):
            self._assert_change_adds(obj, index, elements)

    def _assert_change(self, change_and_elements, index, elements, adds=True):
        change, change_elements = change_and_elements
        length = len(elements)
        if isinstance(index, int):
            slice_ = slice(index, index + length, 1)
        elif isinstance(index, slice):
            slice_ = index
        else:
            raise TypeError("Expected int or slice but not {}".format(index))
        assert change.adds() == adds
        assert change.removes() != adds
        assert change.start == slice_.start
        assert change.stop == slice_.stop
        assert change.length == length
        if adds:
            range_ = range(*slice_.indices(len(self.real)))
        else:
            range_ = range(*slice_.indices(len(self.real_before)))
        assert change.range == range_
        assert change.changed_object is self.observable
        assert change_elements == elements

    def _assert_change_adds(self, obj, index, elements):
        for element in elements:
            assert element in obj
        for i, element in enumerate(elements, index):
            assert obj[i] == element
        assert obj[index:index + len(elements)] == elements

    def assert_remove(self, index, elements):
        self.assert_one_more_change()
        self._assert_change(self.changes_after[-1], index, elements,
                            adds=False)

    def assert_replace(self, index, old_elements, new_elements):
        self.assert_one_more_change(2)
        self._assert_change(self.changes_after[-2], index, old_elements,
                            adds=False)
        self._assert_add(index, new_elements)


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
        return self.call(attr)


@fixture
def chain(ol, changes):
    return ObservableChain([], ol, changes)


@fixture
def filled_chain(chain):
    chain.extend([1, 2, 3, 4])
    return chain


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
        ol.register_observer(observer)
        ol.notify_observers(change)
        observer.assert_called_with(change)

    def test_notify_observers(self, ol, changes):
        change = MagicMock()
        ol.notify_observers(change)
        assert len(changes) == 1
        assert changes[0][0] is change


# To test:
# def __init__(self, initlist=None):
# def __repr__(self):              tested in TestNoChanges
# def __lt__(self, other):         tested in TestNoChanges
# def __le__(self, other):         tested in TestNoChanges
# def __eq__(self, other):         tested in TestNoChanges
# def __gt__(self, other):         tested in TestNoChanges
# def __ge__(self, other):         tested in TestNoChanges
# def __contains__(self, item):    tested in TestNoChanges
# def __len__(self):               tested in TestNoChanges
# def __getitem__(self, i):        tested in TestItemMethods
# def __setitem__(self, i, item):  tested in TestItemMethods
# def __delitem__(self, i):        tested in TestItemMethods
# def __add__(self, other):        tested in TestNoChanges
# def __radd__(self, other):       untested, AttributeError
# def __iadd__(self, other):       tested in TestAddElements
# def __mul__(self, n):            tested in TestAddElements
# __rmul__ = __mul__               tested in TestAddElements
# def __imul__(self, n):           tested in TestAddElements
# def append(self, item):          tested in TestAddElements
# def insert(self, i, item):       tested in TestAddElements
# def pop(self, i=-1):             tested in TestRemoveElements
# def remove(self, item):          tested in TestRemoveElements
# def clear(self):                 tested in TestRemoveElements
# def copy(self):                  tested in TestNoChanges
# def count(self, item):           tested TestNoChanges
# def index(self, item, *args):    tested TestNoChanges
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
        chain.insert(-20, 228).assert_add(0, [228])
        chain.insert(20, 22).assert_add(4, [22])

    @pytest.mark.parametrize("method", ["extend", "__iadd__"])
    def test_extend(self, chain, method):
        chain.call(method)([9, 8, 7, 6]).assert_add(0, [9, 8, 7, 6])
        test = chain.call(method)(lambda: (str(i) for i in range(3)))
        test.assert_add(4, ["0", "1", "2"])
        chain.call(method)(()).assert_no_change()

    def test_imul(self, filled_chain):
        filled_chain.__imul__(3).assert_add(4, [1, 2, 3, 4, 1, 2, 3, 4])
        filled_chain.__imul__("asd").assert_no_change()
        filled_chain.__imul__(1).assert_no_change()

    def test_imul_is_empty(self, chain):
        chain.__imul__(10).assert_no_change()
        chain.__imul__(-10).assert_no_change()
        chain.__imul__(0).assert_no_change()
        chain.__imul__(1).assert_no_change()

    @pytest.mark.parametrize("multiplier", [0, -3])
    def test_imul_deletes(self, filled_chain, multiplier):
        filled_chain.__imul__(multiplier).assert_remove(0, [1, 2, 3, 4])


class TestRemoveElements:

    def test_pop(self, filled_chain):
        filled_chain.pop().assert_remove(3, [4])
        filled_chain.pop(-1).assert_remove(2, [3])

    def test_pop_with_positive_index(self, filled_chain):
        filled_chain.pop(1).assert_remove(1, [2])

    def test_pop_invalid_argument(self, filled_chain):
        filled_chain.pop(-22).assert_no_change()
        filled_chain.pop(22).assert_no_change()
        filled_chain.pop(-6).assert_no_change()
        filled_chain.pop(6).assert_no_change()

    def test_pop_from_empty_list(self, chain):
        chain.pop().assert_no_change()

    def test_pop_type_error(self, filled_chain):
        filled_chain.pop("asd").assert_no_change()

    def test_remove(self, chain):
        chain.extend(range(30))
        chain.remove(10).assert_remove(10, [10])
        chain.remove(10).assert_no_change()

    def test_clear(self, chain):
        chain.clear().assert_no_change()
        chain.extend([1, 2, 3, 4])
        chain.clear().assert_remove(0, [1, 2, 3, 4])
        chain.clear().assert_no_change()


class TestItemMethods:

    def test_delete_fails(self, filled_chain):
        filled_chain.__delitem__(4).assert_no_change()
        filled_chain.__delitem__(-5).assert_no_change()
        filled_chain.__delitem__("123").assert_no_change()

    def test_delete_positive_index_inside(self, filled_chain):
        filled_chain.__delitem__(1).assert_remove(1, [2])

    def test_delete_negative_index_inside(self, filled_chain):
        filled_chain.__delitem__(-1).assert_remove(3, [4])

    def test_delete_slice_inside(self, filled_chain):
        filled_chain.__delitem__(slice(1, 3)).assert_remove(1, [2, 3])

    def test_delete_overlapping_slice(self, filled_chain):
        test = filled_chain.__delitem__(slice(-3, 3, 4))
        test.assert_remove(slice(1, 3, 4), [2])

    @pytest.mark.parametrize("index", [-10, -6, -5, -4, -1, 0, 1, 3, 4, 6, 10])
    def test_getitem(self, filled_chain, index):
        filled_chain.__getitem__(index).assert_no_change()

    def test_setitem(self, filled_chain):
        filled_chain.__setitem__(2, 8).assert_replace(2, [3], [8])


COMPARISONS = ["__lt__", "__le__", "__eq__", "__gt__", "__ge__"]
LISTS = [[1, 2, 3, 2], [2, 3, 4], [0, 1, 2, 3, 4]]
SEARCHES = ["count", "index", "__contains__"]
CONVERSIONS = ["__repr__", "__len__"]


class TestNoChanges:

    def test_copy(self, chain):
        chain.copy().assert_no_change()
        chain.extend([2, 3, 657, 8])
        chain.copy().assert_no_change()

    @pytest.mark.parametrize("method", CONVERSIONS)
    def test_repr(self, chain, method):
        chain.call(method)().assert_no_change()
        chain.extend([1, 2, 3, 4])
        chain.call(method)().assert_no_change()

    @pytest.mark.parametrize("method", COMPARISONS)
    @pytest.mark.parametrize("other", LISTS)
    @pytest.mark.parametrize("elements", LISTS)
    def test_comparisons(self, chain, method, elements, other):
        chain.extend(elements)
        chain.call(method)(other).assert_no_change()

    @pytest.mark.parametrize("method", SEARCHES)
    @pytest.mark.parametrize("element", LISTS[0])
    @pytest.mark.parametrize("elements", LISTS)
    def test_element_search(self, chain, method, elements, element):
        chain.extend(elements)
        chain.call(method)(element).assert_no_change()

    @pytest.mark.parametrize("method", ["__rmul__", "__mul__", "__add__"])
    @pytest.mark.parametrize("parameter", [5, [4], "123"])
    def test_mul(self, chain, method, parameter):
        chain.extend([8, 4, 0, 1])
        chain.call(method)(parameter).assert_no_change()

ALL_METHODS = ["__init__", "__repr__", "__lt__", "__le__", "__eq__", "__gt__",
               "__ge__", "__contains__", "__len__", "__getitem__",
               "__setitem__", "__delitem__", "__add__", "__iadd__",
               "__mul__", "__rmul__", "__imul__", "append", "insert", "pop",
               "remove", "clear", "copy", "count", "index", "reverse", "sort",
               "extend"]


@pytest.mark.parametrize("method", ALL_METHODS)
def test_methods_have_the_description_and_help(method):
    real = getattr(list, method)
    observable = getattr(ObservableList, method)
    assert real.__doc__ == observable.__doc__


def test_initialize_with_list():
    items = (1, 2, 3)
    assert ObservableList(items) == list(items)
