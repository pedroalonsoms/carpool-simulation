import mesa


class CarAgent(mesa.Agent):
    """Un agente para los coches"""

    def __init__(self, unique_id, model, route):
        # Pasar parámetros a la clase padre
        super().__init__(unique_id, model)
        self.route = route
        self.current_index = 0

    def step(self):
        # Avanzar el índice del arreglo de la ruta
        self.current_index += 1
        if self.current_index < len(self.route):
            next_pos = self.route[self.current_index]
            self.model.grid.move_agent(self, next_pos)
