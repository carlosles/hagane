"""Functionality to compute simulations."""
from datetime import datetime, timedelta

from hagane.simulation import Simulation


def step(sim: Simulation) -> Simulation:
    """Return simulation after stepping forward."""
    pass


def run(sim: Simulation, until: int | datetime | timedelta) -> Simulation:
    """Return simulation after running until specified.

    The specified end can be a number of events, a datetime, or a timedelta.
    """
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
