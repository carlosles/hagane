"""Unit tests for statemachine and state functionality."""
from collections import OrderedDict, defaultdict, deque, namedtuple
from dataclasses import field

import pytest
from sortedcontainers import SortedDict, SortedList, SortedSet

from hagane import Statemachine, state, statemachine
from hagane.state import _state


@pytest.fixture
def args():
    """Positional arguments for Foo."""
    return (5,)


@pytest.fixture
def kwargs():
    """Key word arguments for Foo."""
    return {'ys': [1.0, 2.5, 4.6]}


class Foo:
    """A sample standard class."""

    x: int
    ys: list[float] = field(default_factory=list)


@statemachine
class FooMachine:
    """A sample Statemachine class."""

    x: int
    ys: list[float] = field(default_factory=list)


def test_statemachine_decorator(args, kwargs):
    """Test @statemachine class decorator."""
    foo = FooMachine(*args, **kwargs)
    assert foo.__slots__ == ('_change_log', 'x', 'ys')
    assert isinstance(foo, FooMachine)
    assert isinstance(foo, Statemachine)


def test_statemachine_function(args, kwargs):
    """Test @statemachine as a function."""
    cls = statemachine(Foo)
    foo = cls(*args, **kwargs)
    assert foo.__slots__ == ('_change_log', 'x', 'ys')
    assert isinstance(foo, cls)
    assert isinstance(foo, Statemachine)


def test_state(args, kwargs):
    """Test that state() raises a TypeError for non-Statemachine inputs and
    recursively returns the state of Statemachines, including those held in
    linear or hierarchical containers.
    """
    foo = FooMachine(*args, **kwargs)
    with pytest.raises(TypeError):
        state(Foo(*args, **kwargs))
    assert state(foo) == _state(foo)
    assert _state(foo) == {'x': 5, 'ys': [1.0, 2.5, 4.6]}
    assert _state(dict(foo=foo)) == dict(foo=_state(foo))
    assert _state(defaultdict(foo=foo)) == defaultdict(foo=_state(foo))
    assert _state(OrderedDict(foo=foo)) == OrderedDict(foo=_state(foo))
    assert _state(SortedDict(foo=foo)) == SortedDict(foo=_state(foo))
    assert _state(range(5)) == range(5)
    cls = namedtuple('Foo', 'foo')
    assert _state(cls(foo)) == cls(_state(foo))
    assert _state(tuple([foo])) == tuple([_state(foo)])
    assert _state(list([foo])) == list([_state(foo)])
    assert _state(SortedList([foo])) == SortedList([_state(foo)])
    assert _state(deque([foo])) == deque([_state(foo)])
    assert _state(set([-1, 1])) == set(_state([-1, 1]))
    assert _state(SortedSet([-1, 1])) == SortedSet(_state([-1, 1]))
    assert _state(5.8) == 5.8
