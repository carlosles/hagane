"""Functionality to compute simulations."""
from datetime import datetime, timedelta

from hagane.event import Event
from hagane.simulation import Simulation


def step(sim: Simulation) -> Simulation:
    """Return simulation after stepping forward one event."""
    next_event = sim.event_queue.pop(0)
    return handle_event(sim, next_event)


def run(sim: Simulation, until: int | datetime | timedelta) -> Simulation:
    """Return simulation after running until specified.

    The end condition can be a number of events, a datetime, or a timedelta.
    """
    if not sim.event_queue:
        return sim
    match until:
        case int():
            if until == 0:
                return sim
            return run(step(sim), until=until - 1)
        case datetime():
            raise NotImplementedError
        case timedelta():
            raise NotImplementedError
        case _:
            raise TypeError(f'"until" must be {int | datetime | timedelta}')


def rewind(sim: Simulation, until: datetime | timedelta) -> Simulation:
    """Return simulation after rewinding until specified.

    The specified point can be an event number, datetime, or timedelta.
    """
    pass


def handle_event(sim: Simulation, event: Event) -> Simulation:
    """Return simulation after handling event."""
    new_events = event.effect(event.destination)  # type: ignore
    if new_events:
        sim.event_queue.update(new_events)
    return sim
