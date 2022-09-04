"""Exploratory API for coroutine-based event loop processing."""
import asyncio
from collections.abc import Awaitable


async def park(car_aw: Awaitable[int], dt: int) -> int:
    """Park car."""
    car = await car_aw
    print(f'{car}: parking car')
    car += dt
    print(f'{car}: finished parking car')
    return car


async def drive(car_aw: Awaitable[int], dt: int) -> int:
    """Drive car."""
    car = await car_aw
    print(f'{car}: driving car')
    car += dt
    print(f'{car}: finished driving car')
    return car


async def make_car() -> int:
    """Make car."""
    car = 0
    print(f'{car}: creating car')
    print(f'{car}: finished creating car')
    return car


def main() -> None:  # noqa: D103
    car_coro = make_car()
    sim_coro = drive(park(car_coro, dt=5), dt=2)
    result = asyncio.run(sim_coro)
    print(f'{result}: simulation finished')


if __name__ == '__main__':
    main()
