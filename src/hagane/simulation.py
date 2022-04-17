"""Simulation functionality."""
from dataclasses import dataclass, field
from datetime import datetime, timedelta

from sortedcontainers import SortedList

from hagane.event import Event
from hagane.state import Statemachine


@dataclass(frozen=True, slots=True)
class Simulation:
    """Simulation container."""

    components: tuple[Statemachine, ...]
    time: datetime | timedelta = field(default_factory=timedelta)
    event_queue: SortedList[Event] = field(default_factory=SortedList)


# Snapshot
