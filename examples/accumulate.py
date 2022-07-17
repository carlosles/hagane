"""Accumulate script example."""
from itertools import accumulate

data = [
    {'t': 10, 'changes': {'x': 1}},
    {'t': 20, 'changes': {'x': 2}},
    {'t': 30, 'changes': {'x': 3}},
]


def update_state(state: dict, state_change: dict) -> dict:
    s = state['state']
    changes = state_change['changes']
    new_state = {
        't': state_change['t'],
        'state': {k: changes.get(k, v) for k, v in s.items()},
    }
    return new_state


a = accumulate(data, update_state, initial={'t': 0, 'state': {'x': -1}})
list(a)
