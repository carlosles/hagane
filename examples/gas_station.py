"""
Gas station refueling example.

Inspired by Simpy's example:
https://simpy.readthedocs.io/en/latest/examples/gas_station_refuel.html

Covers:
- Resources: Resource
- Resources: Container
- Waiting for other processes

Scenario:
  A gas station has a limited number of gas pumps that share a common
  fuel reservoir. Cars randomly arrive at the gas station, request one
  of the fuel pumps and start refueling from that reservoir.

  A gas station control process observes the gas station's fuel level
  and calls a tank truck for refueling if the station's level drops
  below a threshold.
"""
from __future__ import annotations

import itertools
import random
from dataclasses import field
from functools import partial

import hagane as hg

RANDOM_SEED = 42
GAS_STATION_SIZE = 200  # liters
THRESHOLD = 10  # Threshold for calling the tank truck (in %)
FUEL_TANK_SIZE = 50  # liters
FUEL_TANK_LEVEL = [5, 25]  # Min/max levels of fuel tanks (in liters)
REFUELING_SPEED = 2  # liters / second
TANK_TRUCK_TIME = 300  # Seconds it takes the tank truck to arrive
T_INTER = [30, 300]  # Create a car every [min, max] seconds
SIM_TIME = 1000  # Simulation time in seconds


@hg.statemachine
class GasStation:
    size: float = GAS_STATION_SIZE
    level: float = GAS_STATION_SIZE
    fuel_pump: FuelPump


@hg.statemachine
class FuelPump:
    gas_station: GasStation
    connections: int = 2
    refuel_speed: float = REFUELING_SPEED


@hg.statemachine
class Car:
    fuel_tank_size: float = FUEL_TANK_SIZE
    fuel_tank_level: int = field(
        default_factory=partial(random.randint, *FUEL_TANK_LEVEL)
    )

    @property
    def capacity(self) -> float:
        return self.fuel_tank_size - self.fuel_tank_level


def generate_car(gas_station):
    """Generate new cars that arrive at the gas station."""
    time = random.randint(*T_INTER)
    car = Car()
    return hg.Event(
        name=f'car-{i}',
        effect=partial(refuel_at_station, station=gas_station),
        destination=car,
        trigger_time=time,
    )


def refuel_at_station(car: Car, station: GasStation) -> list[hg.Event]:
    fuel_pump = request_fuel_pump(car, gas_station)
    litres_required = car.capacity
    fuel_pump.gas_station.level -= litres_required
    return [
        hg.Event(name='', duration=litres_required / fuel_pump.refuel_speed)
    ]


def request_fuel_pump(car: Car, station) -> FuelPump:
    pass


@hg.statemachine
class Simulation:
    n_cars: int = 0


if __name__ == '__main__':
    print('Gas Station refuelling')
    random.seed(RANDOM_SEED)

    sim = process(Simulation(), generate_car)
    sim = hg.run(sim, until=10)

    gas_station = []
    fuel_pump = []
    gas_station_control = []
    cars = [Car() for _ in range(5)]

    sim = hg.Simulation(
        components=(*cars,),
        event_queue=[
            hg.Event(
                name='event-1', effect=refuel_at_station, destination=cars
            )
        ],
    )

    sim = hg.run(sim, until=10)
    print(sim)
