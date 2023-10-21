"""Exploratory API for generator-based simulation."""
from collections.abc import Iterable
from dataclasses import dataclass
from itertools import chain, cycle


@dataclass(slots=True)
class Car:
    """Class to represent car that tracks distance travelled."""

    distance: int


time = 0


def timeout(dt: int) -> None:
    """Time out for specified duration."""
    global time
    time += dt


def drive(car: Car, dt: int) -> Iterable[Car]:
    """Drive car."""
    print(f'{time=}: driving, {car}')
    timeout(dt)
    car.distance += 10
    print(f'{time=}: finished driving {car}')
    yield car


def park(car: Car, dt: int) -> Iterable[Car]:
    """Park car."""
    print(f'{time=}: parking, {car}')
    timeout(dt)
    car.distance += 1
    print(f'{time=}: finished parking {car}')
    yield car


def make_car() -> Car:
    """Make car."""
    print(f'{time=}: creating car')
    car = Car(distance=0)
    print(f'{time=}: finished creating {car}')
    yield car


def simulation() -> Iterable[Car]:
    cars = cycle(make_car())
    cars = chain.from_iterable(park(car, dt=5) for car in cars)
    cars = chain.from_iterable(drive(car, dt=2) for car in cars)
    yield from cars


def main() -> None:  # noqa: D103
    global time
    sim = simulation()
    while time < 15:
        car = next(sim)
    result = car
    print(f'{time=}: simulation finished, {result}')


if __name__ == '__main__':
    main()
