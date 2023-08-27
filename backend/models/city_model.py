import json
import os
import mesa
import numpy as np
import random
import constants
from agents.car_agent import CarAgent
from agents.person_agent import PersonAgent


def get_grid(model):
    """Transformar el grid en una representación para que sea leída por matplotlib"""
    grid = np.zeros((model.grid.width, model.grid.height))

    # Creamos arreglo que va a contener los JSON's individuales
    agentJSONs = []
    for agents, (x, y) in model.grid.coord_iter():
        for agent in agents:
            if isinstance(agent, CarAgent):
                grid[x][y] = 2
            if isinstance(agent, PersonAgent):
                grid[x][y] = 1
            # Los vamos agregando a un arreglo
            agentJSONs.append(agent.toJSON())

    # Formateamos los agentes en formato JSON
    stepRawJSON = f"{{ \"data\": [{','.join(agentJSONs)}] }}"
    stepPrettyJSON = json.dumps(json.loads(stepRawJSON), indent=4)

    # Creamos el directorio del output en caso de que no exista
    if not os.path.exists("jsons"):
        os.makedirs("jsons")

    # Escribimos un archivo JSON por cada step que hemos procesado
    with open(f"jsons/{model.step_count}.json", "w") as outfile:
        outfile.write(stepPrettyJSON)

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
        self.step_count = 0

        # Scheduler & recolector de datos
        self.schedule = mesa.time.SimultaneousActivation(self)
        self.grid = mesa.space.MultiGrid(self.height, self.width, False)
        self.datacollector = mesa.DataCollector(model_reporters={"Grid": get_grid})

    def step(self):
        "Avanzar el modelo por un step"

        # Creando coches
        for car_route in constants.car_routes:
            if random.random() < self.car_spawn_rate:
                car = CarAgent(f"Car {self.car_count}", self, car_route)
                self.car_count += 1

        # Creando personas
        for people_station in constants.people_stations.values():
            if random.random() < self.person_spawn_rate:
                person = PersonAgent(f"Person {self.person_count}", self)
                self.grid.place_agent(person, people_station)
                self.schedule.add(person)
                self.person_count += 1

        # Primero le tomamos 'foto' y luego corremos la simulación
        self.datacollector.collect(self)
        self.schedule.step()
        self.step_count += 1
