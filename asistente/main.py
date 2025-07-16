#pylint: disable=line-too-long
"""
Módulo Principal

Permisos necesarios: 'Send Messages' - 'Manage Messages' - "Read Message History" -
                     'Send Messages in Threads' - 'Manage Threads' - 'Mention Everyone' -
                     'Read Messages/View Channels' - 'Add Reactions' - 'Use Slash Commands'

Permissions Integer: 19327560768

Enlace para invitar bot: https://discord.com/api/oauth2/authorize?client_id=889312376036425810&permissions=294205467712&scope=bot%20applications.commands
Repositorio: https://github.com/NLGS2907/Alg1-Lector-de-Ejercicios
"""

from os import getenv

from dotenv import load_dotenv

from .lector import Lector

load_dotenv()


TOKEN = getenv("DISCORD_TOKEN")


def main() -> int:
    "Función principal."

    Lector().run(TOKEN)
    return 0


if __name__ == "__main__":
    main()
