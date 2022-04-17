"""Functional discrete-event simulation."""
from hagane.compute import rewind, run
from hagane.event import Event, EventType
from hagane.simulation import Simulation
from hagane.state import (
    State,
    StateChange,
    Statemachine,
    now,
    state,
    statemachine,
    states,
    update,
)

__version__ = "0.1.0dev"
__all__ = (
    'Event',
    'EventType',
    'Simulation',
    'state',
    'states',
    'State',
    'StateChange',
    'statemachine',
    'Statemachine',
    'now',
    'run',
    'rewind',
    'update',
)
