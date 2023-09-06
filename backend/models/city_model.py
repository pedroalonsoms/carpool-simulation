import json
import mesa
import numpy as np
import random
import constants
from agents.car_agent import CarAgent
from agents.person_agent import PersonAgent


def get_grid(model):
    """Transformar el grid en una representación para que sea leída por matplotlib"""
    grid = np.zeros((model.grid.width, model.grid.height))

    # Creamos arreglo que va a contener los JSON's individuales de cada step
    step_data = {"cars": [], "people": []}
    for agents, (x, y) in model.grid.coord_iter():
        for agent in agents:
            if isinstance(agent, CarAgent):
                # Los vamos agregando a un arreglo
                step_data["cars"].append(agent.toJSON())
                grid[x][y] = 2

            if isinstance(agent, PersonAgent):
                # Los vamos agregando a un arreglo
                step_data["people"].append(agent.toJSON())
                grid[x][y] = 1

    # Guardamos una lista con todos los datos de cada step
    model.simulation_data.append(step_data)
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
        self.people_count = 0
        self.collected_people_count = 0
        self.step_count = 0
        self.simulation_data = []
        self.route_count = [0, 0, 0, 0]

        # Scheduler & recolector de datos
        self.schedule = mesa.time.SimultaneousActivation(self)
        self.grid = mesa.space.MultiGrid(self.height, self.width, False)
        self.datacollector = mesa.DataCollector(model_reporters={"Grid": get_grid})

    def step(self):
        "Avanzar el modelo por un step"

        # Creando coches
        for car_route in constants.car_routes:
            if random.random() < self.car_spawn_rate:
                car = CarAgent(f"CAR_{self.car_count}", self, car_route)
                self.car_count += 1

        # Creando personas
        for people_station in constants.people_stations.values():
            if random.random() < self.person_spawn_rate:
                person = PersonAgent(f"PERSON_{self.people_count}", self)
                self.grid.place_agent(person, people_station)
                self.schedule.add(person)
                self.people_count += 1

        # Primero le tomamos 'foto' y luego corremos la simulación
        self.datacollector.collect(self)
        self.schedule.step()
        self.step_count += 1

    def get_simulation_data_as_json(self):
        # Escribimos un archivo JSON por cada step que hemos procesado
        return {"simulationData": self.simulation_data}
