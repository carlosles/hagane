"""Simulation functionality."""
from collections.abc import Iterable
from dataclasses import dataclass, field
from datetime import datetime, timedelta

from sortedcontainers import SortedList

from hagane.event import Event
from hagane.state import Statemachine


@dataclass(slots=True)
class Simulation:
    """Simulation container."""

    components: tuple[Statemachine, ...]
    time: datetime | timedelta = field(default_factory=timedelta)
    event_queue: SortedList[Event] = field(default_factory=SortedList)

    def __init__(
        self,
        components: tuple[Statemachine, ...],
        time: datetime | timedelta = timedelta(),
        event_queue: Iterable[Event] | None = None,
    ):
        """Initialise simulation instance."""
        self.components = components
        self.time = time
        self.event_queue = SortedList(event_queue)


# Snapshot
# TODO: consider heapq from standard library
