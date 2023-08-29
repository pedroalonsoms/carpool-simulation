import json
import mesa
from agents.person_agent import PersonAgent


class CarAgent(mesa.Agent):
    """Un agente para los coches"""

    def __init__(self, unique_id, model, car_route):
        # Pasar parámetros a la clase padre
        super().__init__(unique_id, model)
        self.car_route = car_route
        self.current_index = 0
        self.planned_passengers = 0
        self.max_passengers = 4

        # Agregamos el coche al tablero
        self.model.schedule.add(self)
        self.model.grid.place_agent(self, car_route["points"][0])

        # Para planear a las personas que va a recoger, checamos por cuáles estaciones pasa el coche
        for people_station in self.car_route["people_stations"]:
            # Vemos cuántas personas hay en este punto en la estación
            people_in_station = self.model.grid.get_cell_list_contents(people_station)
            for person in people_in_station:
                # Si aún no hemos planeado a todos los pasajeros, y hay una persona con car_id nulo
                if (
                    self.planned_passengers < self.max_passengers
                    and person.car_id == None
                ):
                    # Se lo asignamos
                    person.car_id = self.unique_id
                self.planned_passengers += 1

    def step(self):
        # Verificar si alguno de nuestros vecinos es una estación de personas
        neighbors = self.model.grid.get_neighbors(
            self.pos, include_center=False, moore=False
        )
        # Si alguno de los vecinos estaba planeado a ser recogido, se recoge
        for neighbor in neighbors:
            if isinstance(neighbor, PersonAgent) and neighbor.car_id == self.unique_id:
                # Lo sacamos del grid cuando lo encontramos
                self.model.grid.remove_agent(neighbor)

        # Verificamos si está en la última posición de la ruta, si es así, lo eliminamos del tablero
        if self.current_index == len(self.car_route["points"]) - 1:
            self.model.schedule.remove(self)
            self.model.grid.remove_agent(self)

        # Avanzar el índice del arreglo de la ruta
        self.current_index += 1
        if self.current_index < len(self.car_route["points"]):
            next_pos = self.car_route["points"][self.current_index]
            self.model.grid.move_agent(self, next_pos)

    def toJSON(self):
        json_string = f"""
{{
    \"id\": \"{self.unique_id}\", 
    \"type\": \"CAR_AGENT\", 
    \"x\": {self.pos[0]},
    \"y\": {self.pos[1]}
}}"""
        return json.loads(json_string)
