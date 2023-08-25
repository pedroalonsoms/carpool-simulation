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
            if isinstance(agent, PersonAgent):
                grid[x][y] = 1

    return grid


class CityModel(mesa.Model):
    """Tablero de N x M para la ciudad"""

    def __init__(self):
        # El tamaño del tablero es fijo
        self.width = 51
        self.height = 43

        # Scheduler & recolector de datos
        self.schedule = mesa.time.SimultaneousActivation(self)
        self.grid = mesa.space.MultiGrid(self.height, self.width, False)
        self.datacollector = mesa.DataCollector(model_reporters={"Grid": get_grid})

        # Creando personas
        for i in range(20000):
            person = PersonAgent("Person" + str(i), self)
            person_spawn_point = random.choice(constants.people_spawn_points)
            self.grid.place_agent(person, person_spawn_point)

        # Creando coches
        car1 = CarAgent("Car 1", self, constants.car1_road)
        self.schedule.add(car1)
        self.grid.place_agent(car1, (9, 1))

        car2 = CarAgent("Car 2", self, constants.car2_road)
        self.schedule.add(car2)
        self.grid.place_agent(car2, (9, 3))

        car3 = CarAgent("Car 3", self, constants.car3_road)
        self.schedule.add(car3)
        self.grid.place_agent(car3, (9, 5))

        car4 = CarAgent("Car 4", self, constants.car4_road)
        self.schedule.add(car4)
        self.grid.place_agent(car4, (9, 7))

        # Siempre recolectamos una primera 'foto' para saber el estado inicial
        self.datacollector.collect(self)

    def step(self):
        "Avanzar el modelo por un step"

        # Primero corremos la simulación y luego le tomamos 'foto'
        self.schedule.step()
        self.datacollector.collect(self)
