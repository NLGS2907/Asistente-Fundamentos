"Punto de entrada para el paquete del asistente."

from .enviroment import leer_y_cargar_envs

# La carga de variables de entorno debe hacerse primero que nada, incluso primero
# que cualquier import
leer_y_cargar_envs()

from .main import main

if __name__ == "__main__":
    main()