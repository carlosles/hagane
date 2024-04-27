from collections.abc import Generator
from dataclasses import dataclass


@dataclass(slots=True)
class DrivingCar:
    distance: int


@dataclass(slots=True)
class ParkingCar:
    distance: int


@dataclass(slots=True)
class StationaryCar:
    distance: int


time = 0


def timeout(dt: int) -> None:
    """Time out for specified duration."""
    global time
    time += dt


def make_car() -> StationaryCar:
    """Make car."""
    print(f'{time=}: creating car')
    car = StationaryCar(distance=0)
    print(f'{time=}: finished creating {car}')
    return car


def drive(car: StationaryCar | ParkingCar, dt: int) -> DrivingCar:
    """Drive car."""
    print(f'{time=}: driving, {car}')
    car = DrivingCar(distance=car.distance)
    timeout(dt)
    car.distance += 10
    print(f'{time=}: finished driving {car}')
    return car


def park(car: DrivingCar, dt: int) -> StationaryCar:
    """Park car."""
    print(f'{time=}: parking, {car}')
    car = ParkingCar(distance=car.distance)
    timeout(dt)
    car.distance += 1
    print(f'{time=}: finished parking {car}')
    return StationaryCar(distance=car.distance)


def simulation() -> Generator:
    car = make_car()
    while True:
        car = yield drive(car, dt=2)
        car = yield park(car, dt=5)


def run(sim: Generator, until: float) -> Generator:
    global time
    result = None
    while time < until:
        result = sim.send(result)
    print(f'{time=}: simulation finished, {result}')


def main() -> None:
    sim = simulation()
    sim = run(sim, until=15)


if __name__ == '__main__':
    main()

