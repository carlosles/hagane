"""Exploratory API for generator-based simulation."""
from collections.abc import Generator, Iterable
from dataclasses import dataclass


@dataclass(slots=True)
class Car:
    """Class to represent car that tracks distance travelled."""

    distance: int


time = 0


def timeout(dt: int) -> None:
    """Time out for specified duration."""
    global time
    time += dt


def drive(car: Car, dt: int) -> Car:
    """Drive car."""
    print(f'{time=}: driving, {car}')
    timeout(dt)
    car.distance += 10
    print(f'{time=}: finished driving {car}')
    return car


def park(car: Car, dt: int) -> Car:
    """Park car."""
    print(f'{time=}: parking, {car}')
    timeout(dt)
    car.distance += 1
    print(f'{time=}: finished parking {car}')
    return car


def make_car() -> Car:
    """Make car."""
    print(f'{time=}: creating car')
    car = Car(distance=0)
    print(f'{time=}: finished creating {car}')
    return car


def simulation() -> Generator[Car]:
    car = make_car()
    while True:
        car = yield park(car, dt=5)
        car = yield drive(car, dt=2)


def main() -> None:  # noqa: D103
    sim = simulation()
    # for car in sim:
    # while car := next(sim):
    # car = next(sim)
    car = None
    while time < 15:
        car = sim.send(car)
    result = car
    print(f'{time=}: simulation finished, {result}')


if __name__ == '__main__':
    main()
