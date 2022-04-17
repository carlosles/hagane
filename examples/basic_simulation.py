from datetime import timedelta

import hagane as hg


@hg.statemachine
class Tank:
    """Tank statemachine."""

    name: str
    status: str = 'operational'
    damage: float = 0
    capacity: float = 60
    fuel: float = 45


@hg.statemachine
class Car:
    """Car statemachine."""

    name: str
    tank: Tank
    status: str = 'operational'
    damage: float = 0


def main():
    """Run script."""
    tank = Tank(name='tank_1')
    car = Car(name='car_1', tank=tank)
    sim = hg.Simulation(components=(car,))
    forwarded = hg.run(sim, until=timedelta(days=1))
    rewinded = hg.rewind(forwarded, until=timedelta(hours=12))
    print(rewinded)


if __name__ == '__main__':
    main()
