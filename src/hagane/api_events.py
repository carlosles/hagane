"""Exploratory API using events."""

from collections.abc import Iterator
from heapq import heappop, heappush
from itertools import chain, count
import sys

from more_itertools import take


type Process = Iterator[Event]
type Event = tuple[float, int, Process]

eids = count()
queue: list[Event] = []
x = 0.0


def run_sim(*processes):
    global queue, x

    for process in processes:
        heappush(queue, (0.0, next(eids), process))
    while queue:
        event = heappop(queue)
        yield event
        x, _, process = event
        next_x, next_eid, next_process = next(process)
        next_event = (next_x, next_eid, chain(next_process, process))
        heappush(queue, next_event)


def defer_until(process: Process, until: float) -> Event:
    return (until, next(eids), process)


def defer_for(process: Process, dx: float) -> Event:
    return (x + dx, next(eids), process)


def wait_for(dx: float) -> Event:
    return (x + dx, next(eids), nothing())


def nothing() -> Process:
    yield from ()


def run_car() -> Process:
    while True:
        # Commented lines below are equivalent to those underneath.
        #yield defer_for(drive_car(), 10.0)
        #yield defer_for(park_car(), 3.0)
        yield from drive_car()
        yield wait_for(10.0)
        yield from park_car()
        yield wait_for(3.0)


def drive_car() -> Process:
    yield from ()


def park_car() -> Process:
    yield from ()


def main(*args):
    n_events = int(args[1]) if len(args) > 1 else 10
    events = run_sim(run_car())
    for event in take(n_events, events):
        print(event)


if __name__ == '__main__':
    main(*sys.argv)

