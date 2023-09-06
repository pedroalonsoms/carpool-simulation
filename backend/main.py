"""
Codigo Reto Final: Simulación de Carpooling

Equipo 2
Angela Sofía Pontón Ochoa A01284845
Felipe de Jesus González Acosta A01275536
Pedro Alonso Moreno Salcedo A01741437
Daniel Arguedas Alvarado A00829735

5 de septiembre de 2023
"""

from models.city_model import CityModel
from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route("/")
def index():
    # Creamos una instancia del modelo
    car_spawn_rate = float(request.args.get("car_spawn_rate"))
    person_spawn_rate = float(request.args.get("person_spawn_rate"))

    model = CityModel(car_spawn_rate, person_spawn_rate)

    # Mientras no hayamos excedido el número máximo de datos, correr la simulación
    max_steps = 100
    i = 0
    while i < max_steps:
        model.step()
        i += 1

    # Imprimimos la cantidad de coches y personas finales
    print("====")
    print("Final people_count", model.people_count)
    print("Final collected_people_count", model.collected_people_count)
    print("Ratio", round(model.collected_people_count * 100 / model.people_count), "%")
    print("====")
    print("Final car_count", model.car_count)
    print("====")

    # Guardar lo que sucedió en la simulación como JSON
    return jsonify(model.get_simulation_data_as_json())


if __name__ == "__main__":
    app.run(debug=False)
