"""Statemachine and state functionality."""
import copy
from abc import ABC
from collections import deque
from collections.abc import Collection, Iterator, Mapping
from dataclasses import dataclass, field, fields, make_dataclass, replace
from datetime import datetime, timedelta
from functools import wraps
from typing import Any

from sortedcontainers import SortedList

# from itertools import accumulate


# The name of the class attribute that stores the state changes.
_STATE_LOG = '_change_log'


# @dataclass(frozen=True, slots=True)
# class State:
#    time: datetime | timedelta
State = dict[str, Any]


@dataclass(frozen=True, slots=True)
class StateChange:
    """State change container."""

    time: datetime | timedelta
    change_map: dict[str, Any]


@dataclass(slots=True)
class Statemachine(ABC):
    """Statemachine container."""

    _process_queue: SortedList[Process] = field(
        default_factory=SortedList, kw_only=True, repr=False
    )
    _change_log: deque[StateChange] = field(
        default_factory=deque, kw_only=True, repr=False
    )


def statemachine(cls: type) -> type:
    """Statemachine class decorator."""

    @wraps(cls)
    def wrap(_cls: type) -> type:
        return _process_class(_cls)

    return wrap(cls)


def _process_class(cls: type) -> type:
    return make_dataclass(
        cls_name=cls.__name__,
        fields=[(f.name, f.type, f) for f in fields(dataclass(cls))],
        bases=(Statemachine,),
        slots=True,
    )


def now(sm: Statemachine) -> datetime | timedelta:
    """Return current simulation time."""
    # TODO: implement.
    pass


def update(sm: Statemachine, **changes: Any) -> Statemachine:
    """Return statemachine updated with changes."""
    # TODO: log initial state correctly.
    state_change = StateChange(time=now(sm), change_map=changes)
    sm._change_log.append(state_change)
    return replace(sm, **changes)


def states(
    sm: Statemachine, at: datetime | timedelta | None = None
) -> tuple[State, ...]:
    """Return tuple of all past states of statemachine."""
    # TODO: implement and use `at` optional argument.
    # accumulate(reversed(sm._change_log), func=replace, initial=sm)
    # return tuple(map(_state, reversed(sm._change_log)))
    if at is not None:
        raise NotImplementedError
    # initial_sm = type(sm)()
    return tuple()


def state(sm: Statemachine) -> State:
    """Return statemachine state as a dictionary mapping field names to values.

    The function applies recursively to field values that are statemachines,
    mappings, or collections. The function implementation is similar to that
    of the `dataclasses.asdict()` function.
    """
    match sm:
        case Statemachine():
            return _state(sm)  # type: ignore
        case _:
            raise TypeError('state() must be called on statemachines')


def _slots(sm: Statemachine) -> Iterator[str]:
    return (s for s in getattr(sm, '__slots__') if s != _STATE_LOG)


def _state(obj: Any) -> Any:
    # TODO: support other collections that don't initialise from iterable.
    match obj:
        case Statemachine():
            return {s: _state(getattr(obj, s)) for s in _slots(obj)}
        case Mapping():
            return type(obj)(**{k: _state(v) for k, v in obj.items()})
        case range():
            return obj
        case tuple() if hasattr(obj, '_fields'):  # obj is a namedtuple
            return type(obj)(*(_state(v) for v in obj))
        case Collection():
            return type(obj)(_state(v) for v in obj)  # type: ignore[call-arg]
        case _:
            return copy.deepcopy(obj)


# def event_loop(sm: Statemachine):
#     # TODO: implement.
#     pass


# state_log = [
#    {
#        'damage': 50,
#        'tank': {
#            'damage': 20,
#            'capacity': 60,
#        }
#    }
# ]
# event_log = [
#    {
#        't': 1200,
#        'car': {
#            't': 3600,
#            'damage': 50,
#            'tank': {
#                'damage': 20,
#                'capacity': 60,
#            },
#        },
#        'weather': {
#            't': 3810,
#            'temperature': 15,
#            'humidity': 0.75,
#        },
#    },
# ]
