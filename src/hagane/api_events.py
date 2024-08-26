"""Exploratory API using events."""

from collections import deque
from collections.abc import Iterator
from heapq import heappop, heappush
from itertools import chain, count, islice
import sys


type Process = Iterator[Event]
type Event = tuple[float, int, deque[Process]]

eids = count(start=1)
queue: list[Event] = []
x = 0.0


def run_sim(*processes: Process) -> Process:
    global queue, x

    for proc in processes:
        heappush(queue, (x, next(eids), deque([proc])))
    while queue:
        event = heappop(queue)
        yield event
        x, _, processes = event
        try:
            process = processes.popleft()
            next_x, next_eid, next_processes = next(process)
            next_processes.append(process)
            next_processes.extend(processes)
            next_event = (next_x, next_eid, next_processes)
            heappush(queue, next_event)
        except (IndexError, StopIteration):
            pass  # Do nothing.


def defer_until(process: Process, until: float) -> Event:
    return (until, next(eids), deque(process))


def defer_for(process: Process, dx: float) -> Event:
    return (x + dx, next(eids), deque(process))


def wait_for(dx: float) -> Event:
    return (x + dx, next(eids), deque(nothing()))


def nothing():
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
    for event in islice(events, n_events):
        print(event)


if __name__ == '__main__':
    main(*sys.argv)

