import json
import mesa


class PersonAgent(mesa.Agent):
    """Un agente para las personas en general"""

    def __init__(self, unique_id, model):
        # Pasar parámetros a la clase padre
        super().__init__(unique_id, model)
        self.car_id = None

    def step(self):
        "Agente pasivo"
        pass

    def toJSON(self):
        json_string = f"""
{{
    \"id\": \"{self.unique_id}\",
    \"x\": {self.pos[0]},
    \"y\": {self.pos[1]}
}}"""
        return json.loads(json_string)
