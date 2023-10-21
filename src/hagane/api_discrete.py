from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, field
from functools import partial, wraps
from typing import Any, Union


def run(sm: StateMachine, until: int | None = None) -> StateMachine:
    if not sm._process_queue or (until is not None and time(sm) >= until):
        return sm
    return run(step(sm), until=until)


def step(sm: StateMachine) -> StateMachine:
    next_process = sm._process_queue.pop(0)
    return execute_process(sm, next_process)


def execute_process(sm: StateMachine, process: Process) -> StateMachine:
    return process(sm)


def state(sm: StateMachine, at: int | None = None) -> State:
    pass


def time(sm: StateMachine) -> int:
    return sm._change_log[-1].time if sm._change_log else 0


def add(sm: StateMachine, proc: Process) -> StateMachine:
    sm._process_queue.append(proc)
    return sm


# Decorator.
def process(func: Callable[[StateMachine, Any], StateMachine]) -> Process:
    @wraps(func)
    def wrap(sm: StateMachine, *args: Any, **kwargs: Any) -> StateMachine:
        return add(sm, partial(func, *args, **kwargs))

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
    _change_log: list[StateChange] = field(
        default_factory=list, kw_only=True, repr=False
    )
    _process_queue: list[Process] = field(
        default_factory=list, kw_only=True, repr=False
    )

    # def __post_init__(self):
    #     StateMachine.__setattr__ = tracking(self.__setattr__)

    def __setattr__(self, __name: str, __value: Any) -> None:
        if hasattr(self, '_change_log'):
            self = change(self, change_map={__name: __value})
        object.__setattr__(self, __name, __value)


# State = dict[str, Any]
@dataclass(slots=True)
class State:
    pass


Process = Callable[[StateMachine], StateMachine]
# @dataclass(slots=True)
# class Process:
#     start: int
#     end: int
#     effect: Callable[[Any], list[Process]]


@dataclass(slots=True, frozen=True)
class StateChange:
    time: int
    change_map: dict[str, Any]


@process
def park(sm: StateMachine) -> StateMachine:
    return timeout(sm, duration=5)


@process
def drive(sm: StateMachine) -> StateMachine:
    return timeout(sm, duration=2)


@process
def double_x(car: Car) -> Car:
    car.x = car.x * 2
    return car


@process
def run_car(car: Car) -> Car:
    return run_car(double_x(drive(park(car))))


@dataclass(slots=True)
class Car(StateMachine):
    x: int = 1


# Car = StateMachine


@dataclass(slots=True)
class Fleet(StateMachine):
    cars: list[Car] = field(default_factory=list)


def main() -> None:
    # Example 1: a car that parks and drives.
    car = run_car(Car())
    car = run(car, until=15)
    # car.x = 5

    # Example 2: a fleet of cars that park and drive.
    fleet = Fleet([park(Car()) for _ in range(3)])
    fleet = run(fleet, until=15)


if __name__ == '__main__':
    main()
