"""Event functionality."""
from collections.abc import Callable
from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum
from typing import Any


class EventType(Enum):
    """Event types enumeration."""

    pass


@dataclass(frozen=True, slots=True)
class Event:
    """Event container."""

    name: str
    source: str
    destination: str
    effect: Callable[[Any], Any]
    trigger_time: datetime
    duration: timedelta
