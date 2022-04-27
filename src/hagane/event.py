"""Event functionality."""
from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum
from typing import Any

from hagane.state import Statemachine


class EventType(Enum):
    """Event types enumeration."""

    pass


@dataclass(frozen=True, slots=True)
class Event:
    """Event container."""

    name: str
    effect: Callable[[Any], list[Event]]
    source: Statemachine | None = None
    destination: Statemachine | None = None
    trigger_time: datetime | timedelta | None = None
    duration: timedelta | None = None
