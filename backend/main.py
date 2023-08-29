"""
Codigo Reto Final: Simulación de Carpooling

Equipo 2
Angela Sofía Pontón Ochoa A01284845
Felipe de Jesus González Acosta A01275536
Pedro Alonso Moreno Salcedo A01741437
Daniel Arguedas Alvarado A00829735

20 de agosto de 2023
"""

# Gráficas
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.animation as animation

from models.city_model import CityModel


def main():
    # Creamos una instancia del modelo
    car_spawn_rate = 0.7
    person_spawn_rate = 0.2
    model = CityModel(car_spawn_rate, person_spawn_rate)

    # Mientras no hayamos excedido el número máximo de datos, correr la simulación
    max_steps = 100
    i = 0
    while i < max_steps:
        model.step()
        i += 1

    # Guardar lo que sucedió en la simulación como JSON
    model.save_steps_data_as_json()

    # Recolectamos todas las 'fotos'
    all_grid = model.datacollector.get_model_vars_dataframe()

    # Mostramos la gráfica
    plt.rcParams["animation.html"] = "jshtml"
    matplotlib.rcParams["animation.embed_limit"] = 2**128

    fig, axs = plt.subplots(figsize=(7, 7))
    axs.set_xticks([])
    axs.set_yticks([])
    patch = plt.imshow(all_grid.iloc[0][0], cmap=plt.cm.binary)

    def animate(i):
        patch.set_data(all_grid.iloc[i][0])

    anim = animation.FuncAnimation(fig, animate, frames=len(all_grid))
    plt.show()


if __name__ == "__main__":
    main()
