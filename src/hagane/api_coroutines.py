"""Exploratory API for coroutine-based event loop processing."""
import asyncio
from collections.abc import Awaitable
from dataclasses import dataclass


@dataclass(slots=True)
class Car:
    """Class to represent car that tracks distance travelled."""

    distance: int


time = 0
waiting: asyncio.PriorityQueue[int] = asyncio.PriorityQueue()


async def timeout(dt: int) -> None:
    """Time out for specified duration."""
    global time
    until = time + dt
    await waiting.put(until)
    while time < until:
        time = await waiting.get()


async def park(car_aw: Awaitable[Car], dt: int) -> Car:
    """Park car."""
    car = await car_aw
    print(f'{time=}: parking, {car}')
    await timeout(dt)
    car.distance += 1
    print(f'{time=}: finished parking {car}')
    return car


async def drive(car_aw: Awaitable[Car], dt: int) -> Car:
    """Drive car."""
    car = await car_aw
    print(f'{time=}: driving, {car}')
    await timeout(dt)
    car.distance += 10
    print(f'{time=}: finished driving {car}')
    return car


async def make_car() -> Car:
    """Make car."""
    print(f'{time=}: creating car')
    car = Car(distance=0)
    print(f'{time=}: finished creating {car}')
    return car


def main() -> None:  # noqa: D103
    sim_coro = drive(park(make_car(), dt=5), dt=2)
    result = asyncio.run(sim_coro)
    print(f'{time=}: simulation finished, {result}')


if __name__ == '__main__':
    main()
