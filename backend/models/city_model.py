import mesa
import numpy as np
import random
import constants
from agents.car_agent import CarAgent
from agents.person_agent import PersonAgent


def get_grid(model):
    """Transformar el grid en una representación para que sea leída por matplotlib"""
    grid = np.zeros((model.grid.width, model.grid.height))

    for agents, (x, y) in model.grid.coord_iter():
        for agent in agents:
            if isinstance(agent, CarAgent):
                grid[x][y] = 2
        for agent in agents:
            if isinstance(agent, PersonAgent):
                grid[x][y] = 1

    return grid


class CityModel(mesa.Model):
    """Tablero de N x M para la ciudad"""

    def __init__(self, car_spawn_rate, person_spawn_rate):
        # El tamaño del tablero es fijo
        self.width = 51
        self.height = 43
        self.car_spawn_rate = car_spawn_rate
        self.person_spawn_rate = person_spawn_rate
        self.car_count = 0
        self.person_count = 0

        # Scheduler & recolector de datos
        self.schedule = mesa.time.SimultaneousActivation(self)
        self.grid = mesa.space.MultiGrid(self.height, self.width, False)
        self.datacollector = mesa.DataCollector(model_reporters={"Grid": get_grid})

    def step(self):
        "Avanzar el modelo por un step"

        # Creando coches
        for car_road in constants.car_roads:
            if random.random() < self.car_spawn_rate:
                car = CarAgent(f"Car {self.car_count}", self, car_road)
                self.grid.place_agent(car, car_road[0])
                self.schedule.add(car)
                self.car_count += 1

        # Creando personas
        for spawn_point in constants.people_spawn_points:
            if random.random() < self.person_spawn_rate:
                person = PersonAgent(f"Person {self.person_count}", self)
                self.grid.place_agent(person, spawn_point)
                self.schedule.add(person)
                self.person_count += 1

        # Primero corremos la simulación y luego le tomamos 'foto'
        self.schedule.step()
        self.datacollector.collect(self)
