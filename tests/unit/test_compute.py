"""Unit tests for simulation computing functionality."""
from dataclasses import field

import pytest
from sortedcontainers import SortedList

from hagane import Event, Simulation, run, statemachine


@statemachine
class Foo:
    """A sample Statemachine class."""

    x: int
    ys: list[float] = field(default_factory=list)


def sample_func(foo: Foo) -> list[Event]:
    """Perform an event effect."""
    foo.ys.append(foo.ys[-1] + 1 if foo.ys else 1)
    return [Event('event-x', sample_func, destination=foo)]


@pytest.fixture
def simulation() -> Simulation:
    """Return a sample simulation."""
    foo = Foo(1)
    components = tuple([foo])
    events = SortedList(
        [
            Event(name='event-1', effect=sample_func, destination=foo),
        ]
    )
    return Simulation(components, event_queue=events)


def test_run_simulation(simulation):
    """Test run()."""
    sim = run(simulation, until=10)
    assert len(sim.components[-1].ys) == 10
    assert sim.components[-1].ys == list(range(1, 11))
