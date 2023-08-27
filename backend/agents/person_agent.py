import mesa


class PersonAgent(mesa.Agent):
    """Un agente para las personas en general"""

    def __init__(self, unique_id, model):
        # Pasar parámetros a la clase padre
        super().__init__(unique_id, model)
        self.car_id = None

    def step(self):
        pass

    def toJSON(self):
        return f"""
{{
    \"id\": \"{self.unique_id}\",
    \"type\": \"PERSON_AGENT\", 
    \"x\": {self.pos[0]},
    \"y\": {self.pos[1]}
}}"""
