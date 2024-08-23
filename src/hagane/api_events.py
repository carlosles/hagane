"""Exploratory API using events."""

from collections.abc import Iterator
from heapq import heappop, heappush
from itertools import chain, count
import sys

from more_itertools import take


type Process = Iterator[Event]
type Event = tuple[float, Process, int]

eids = count()
queue: list[Event] = []
x = 0.0


def run_sim(*processes):
    global queue, x

    for process in processes:
        heappush(queue, (0.0, process, next(eids)))
    while queue:
        event = heappop(queue)
        yield event
        x, process, _ = event
        next_x, next_process, next_eid = next(process)
        next_event = (next_x, chain(next_process, process), next_eid)
        heappush(queue, next_event)


def defer_until(process: Process, until: float) -> Event:
    return (until, process, next(eids))


def defer_for(process: Process, dx: float) -> Event:
    return (x + dx, process, next(eids))


def run_car() -> Iterator[Event]:
    while True:
        yield defer_for(drive_car(), 10.0)
        yield defer_for(park_car(), 3.0)


def drive_car() -> Iterator[Event]:
    yield from ()


def park_car() -> Iterator[Event]:
    yield from ()


def main(*args):
    n_events = int(args[1]) if len(args) > 1 else 10
    events = run_sim(run_car())
    for event in take(n_events, events):
        print(event)


if __name__ == '__main__':
    main(*sys.argv)

