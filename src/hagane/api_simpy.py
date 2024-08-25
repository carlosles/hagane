"""Benchmark Simpy API."""

import sys

import simpy


def run_car(env: simpy.Environment):
    while True:
        yield env.process(drive_car())
        yield env.timeout(10.0)
        yield env.process(park_car())
        yield env.timeout(3.0)


def drive_car():
    yield from ()


def park_car():
    yield from ()


def main(*args):
    n_events = int(args[1]) if len(args) > 1 else 10
    env = simpy.Environment()
    env.process(run_car(env))
    for ii in range(n_events):
        event = (env.now, ii, env.step())
        print(event)


if __name__ == '__main__':
    main(*sys.argv)

