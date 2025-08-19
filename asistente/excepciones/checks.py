"Módulo que incluye excepciones personalizadas de app checks de Discord."

from discord.app_commands import CheckFailure


class SessionNotSetUp(CheckFailure):
    "La sesión que se conecta al backend de fundamentos no está propiamente inicializada."
