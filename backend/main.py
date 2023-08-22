"""
Codigo Reto Final: Simulación de Carpooling

Equipo 2
Angela Sofía Pontón Ochoa A01284845
Felipe de Jesus González Acosta A01275536
Pedro Alonso Moreno Salcedo A01741437
Daniel Arguedas Alvarado A00829735

20 de agosto de 2023
"""

# Framework de mesa
import mesa

# Arrays y matrices de múltiples dimensiones
import numpy as np

# Randomización
import random

# Gráficas
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.animation as animation


def get_grid(model):
    """Transformar el grid en una representación para que sea leída por matplotlib"""
    grid = np.zeros((model.grid.width, model.grid.height))

    for agents, (x, y) in model.grid.coord_iter():
        for agent in agents:
            if isinstance(agent, CarAgent):
                grid[x][y] = 1
            if isinstance(agent, PersonAgent):
                grid[x][y] = 2

    return grid


class CarAgent(mesa.Agent):
    """Un agente para los coches"""

    def __init__(self, unique_id, model, route):
        # Pasar parámetros a la clase padre
        super().__init__(unique_id, model)
        self.route = route
        self.current_index = 0

    def step(self):
        self.current_index += 1
        if self.current_index < len(self.route):
            next_pos = self.route[self.current_index]
            self.model.grid.move_agent(self, next_pos)


class PersonAgent(mesa.Agent):
    """Un agente para las personas en general"""

    def __init__(self, unique_id, model):
        # Pasar parámetros a la clase padre
        super().__init__(unique_id, model)


class CityModel(mesa.Model):
    """Tablero de N x M para la ciudad"""

    def __init__(self):
        # El tamaño del tablero es fijo
        self.width = 10
        self.height = 10

        # Scheduler & recolector de datos
        self.schedule = mesa.time.SimultaneousActivation(self)
        self.grid = mesa.space.MultiGrid(self.width, self.height, False)
        self.datacollector = mesa.DataCollector(model_reporters={"Grid": get_grid})

        # Creando personas
        for i in range(7):
            person = PersonAgent("Person" + str(i), self)
            self.grid.place_agent(person, (0, 0))
            self.grid.move_to_empty(person)

        # Creando coches
        car1 = CarAgent(
            "Car 1",
            self,
            [
                (9, 1),
                (8, 1),
                (7, 1),
                (6, 1),
                (5, 1),
                (4, 1),
                (3, 1),
                (2, 1),
                (1, 1),
                (0, 1),
            ],
        )
        self.schedule.add(car1)
        self.grid.place_agent(car1, (9, 1))

        car2 = CarAgent(
            "Car 2",
            self,
            [
                (9, 3),
                (8, 3),
                (7, 3),
                (6, 3),
                (5, 3),
                (4, 3),
                (3, 3),
                (2, 3),
                (1, 3),
                (0, 3),
            ],
        )
        self.schedule.add(car2)
        self.grid.place_agent(car2, (9, 3))

        car3 = CarAgent(
            "Car 3",
            self,
            [
                (9, 5),
                (8, 5),
                (7, 5),
                (6, 5),
                (5, 5),
                (4, 5),
                (3, 5),
                (2, 5),
                (1, 5),
                (0, 5),
            ],
        )
        self.schedule.add(car3)
        self.grid.place_agent(car3, (9, 5))

        car4 = CarAgent(
            "Car 4",
            self,
            [
                (9, 7),
                (8, 7),
                (7, 7),
                (6, 7),
                (5, 7),
                (4, 7),
                (3, 7),
                (2, 7),
                (1, 7),
                (0, 7),
            ],
        )
        self.schedule.add(car4)
        self.grid.place_agent(car4, (9, 7))

        # Siempre recolectamos una primera 'foto' para saber el estado inicial
        self.datacollector.collect(self)

    def step(self):
        "Avanzar el modelo por un step"

        # Primero corremos la simulación y luego le tomamos 'foto'
        self.schedule.step()
        self.datacollector.collect(self)


print("HELLO")
