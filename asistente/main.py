"Módulo Principal."

from os import getenv

from .bot import Asistente
from .db import init_database
from .logger import AssistLogger

TOKEN = getenv("DISCORD_TOKEN")


def main(*args: str) -> int:
    "Función principal."

    sep = "=" * 25
    AssistLogger().info(f"{sep} Iniciando Asistente {sep}")

    init_database()
    Asistente(
        verbose=("-v" in args or "--verbose" in args)
    ).run(TOKEN, log_handler=None) # El handler lo seteamos a mano antes

    return 0


if __name__ == "__main__":
    main()
