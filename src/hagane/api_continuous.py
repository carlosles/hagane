from __future__ import annotations

from collections.abc import Callable, Iterator
from dataclasses import dataclass, field
from functools import partial, wraps
from typing import Any, Union


def run(sm: StateMachine, until: int | None = None) -> StateMachine:
    if not sm.process_queue or (until is not None and time(sm) >= until):
        return sm
    return run(step(sm), until=until)


def step(sm: StateMachine) -> StateMachine:
    next_process = sm.process_queue.pop(0)
    return execute_process(sm, next_process)


def execute_process(sm: StateMachine, process: Process) -> StateMachine:
    return process.func(sm, process.dt)


def state(sm: StateMachine, at: int | None = None) -> State:
    pass


def time(sm: StateMachine) -> int:
    return sm._change_log[-1].time if sm._change_log else 0


def add(sm: StateMachine, proc: Process) -> StateMachine:
    sm.process_queue.append(proc)
    return sm


# Decorator.
def process(
    func: Callable[[StateMachine, int, Any], StateMachine],
    # start: int | Callable | None = None,
    # duration: int | Callable | None = None,
) -> Callable[[StateMachine, int, Any], StateMachine]:
    @wraps(func)
    def wrap(
        sm: StateMachine, dt: int = 0, *args: Any, **kwargs: Any
    ) -> StateMachine:
        return add(sm, Process(partial(func, *args, **kwargs), dt))

    return wrap


# Decorator.
def event(
    func: Callable[[StateMachine, Any], StateMachine],
) -> Callable[[StateMachine, Any], StateMachine]:
    @wraps(func)
    def wrap(sm: StateMachine, *args: Any, **kwargs: Any) -> StateMachine:
        return add(sm, Process(lambda _: partial(func, *args, **kwargs), 0))

    return wrap


@process
def timeout(sm: StateMachine, duration: int) -> StateMachine:
    # return add(sm, Process(start=time(sm), end=time(sm) + 5,  effect=timeout))
    return change(sm, duration=duration)


def change(
    sm: StateMachine,
    change_map: dict[str, Any] | None = None,
    duration: int = 0,
) -> StateMachine:
    sm._change_log.append(StateChange(time(sm) + duration, change_map))
    if change_map is not None:
        for k, v in change_map.items():
            setattr(sm, k, partial(v, _sm=sm))
    return sm


# p = Union[add, timeout, change]


def tracking(func: Callable) -> Callable:
    @wraps(func)
    def wrap(sm: StateMachine, __name: str, __value: Any) -> Callable:
        sm = change(sm, change_map={__name: __value})
        return func(__name, __value)

    return wrap


@dataclass(slots=True)
class StateMachine:
    process_queue: list[Process] = field(default_factory=list, repr=False)
    _change_log: list[StateChange] = field(
        default_factory=list, kw_only=True, repr=False
    )

    # def __post_init__(self):
    #     StateMachine.__setattr__ = tracking(self.__setattr__)

    # def __setattr__(self, __name: str, __value: Any) -> None:
    # if hasattr(self, '_change_log'):
    # self = change(self, change_map={__name: __value})
    # object.__setattr__(self, __name, __value)


# State = dict[str, Any]
@dataclass(slots=True)
class State:
    pass


# Process = Callable[[StateMachine], StateMachine]
@dataclass(slots=True)
class Process:
    func: Callable[[StateMachine, int, Any], StateMachine]
    dt: int


@dataclass(slots=True, frozen=True)
class StateChange:
    time: int
    change_map: dict[str, Any]


@process
def park(sm: StateMachine, dt: int) -> StateMachine:
    return timeout(sm, dt=dt)


@process
def drive(sm: StateMachine, dt: int) -> StateMachine:
    # sm.x += 0.5 * dt
    # sm.x = Process(lambda x, t: x + 0.5 * (t - time(sm)), dt)
    # sm.x = lambda t: sm.x(t) + 0.5 * min(dt, t - time(sm))
    func = lambda t: sm.x(t) + 0.5 * min(dt, t - time(sm))
    sm = process(change)(sm, change_map={'x': func})
    return timeout(sm, dt=dt)


@process
def run_car(car: Car, dt: int = 0) -> Car:
    return run_car(drive(park(car, dt=5), dt=2))


@dataclass(slots=True)
class Car(StateMachine):
    x: int = 0


# Car = StateMachine


@dataclass(slots=True)
class Fleet(StateMachine):
    cars: list[Car] = field(default_factory=list)


def main() -> None:
    # Example 1: a car that parks and drives.
    car = run_car(Car())
    car = run(car, until=15)
    car.x = 5

    # Example 2: a fleet of cars that park and drive.
    fleet = Fleet([park(Car()) for _ in range(3)])
    fleet = run(fleet, until=15)


if __name__ == '__main__':
    main()
