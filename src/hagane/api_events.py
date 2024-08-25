"""Exploratory API using events."""

from collections.abc import Iterator
from heapq import heappop, heappush
from itertools import chain, count, islice
import sys


type Process = Iterator[Event]
type Event = WaitEvent | ProcessEvent
type WaitEvent = tuple[float, int]
type ProcessEvent = tuple[float, int, Process]

eids = count(start=1)
queue: list[Event] = []
x = 0.0


def run_sim(*processes: Process) -> Process:
    global queue, x

    for proc in processes:
        heappush(queue, (x, next(eids), proc))
    while queue:
        event = heappop(queue)
        yield event
        x, _, process = event
        try:
            match next(process):
                case (next_x, eid) as wait_event:  # A wait event.
                    yield wait_event
                    next_event = (next_x, next(eids), process)
                case (next_x, eid, next_process):  # A process event.
                    next_event = (next_x, eid, chain(next_process, process))
                case invalid_event:
                    raise ValueError(f'Invalid event {invalid_event}')
            heappush(queue, next_event)
        except StopIteration:
            pass  # Do nothing.


def defer_until(process: Process, until: float) -> ProcessEvent:
    return (until, next(eids), process)


def defer_for(process: Process, dx: float) -> ProcessEvent:
    return (x + dx, next(eids), process)


def wait_for(dx: float) -> WaitEvent:
    return (x + dx, next(eids))


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

