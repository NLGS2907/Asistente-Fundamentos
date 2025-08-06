"""
Registrador de eventos.
"""

from logging import DEBUG, INFO, FileHandler, Formatter, StreamHandler, getLogger
from threading import Lock
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:

    from logging import Logger
    from os import PathLike

LOG_PATH: "PathLike" = "./asistente.log"
"La ruta en donde se guarda el archivo de log."


class AssistLogger:
    """
    Clase que registra eventos del bot.
    Se utiliza un patrón Singleton para asegurar de que se pueda usar globalmente sin
    dejar registros duplicados.
    """

    __instancia: Optional["AssistLogger"] = None
    __lock: Lock = Lock()


    def __new__(cls, *args, **kwargs) -> "AssistLogger":
        """
        Crea una instancia del logger si no existe todavía. Si ya existe, devuelve la
        misma instancia siempre.
        """

        # Esta comparación es para que otros hilos no pierdan tiempo esperando si
        # la instancia ya fue creada
        if cls.__instancia is None:
            with cls.__lock:
                # Y esta comparación es en el caso especial en que más de un hilo se quede
                # esperando porque pidieron el lock a la vez
                if cls.__instancia is None:
                    cls.__instancia = super().__new__(cls)

        return cls.__instancia


    def __init__(self,
                 *,
                 nombre_log: str="asistente",
                 nivel_arch: int=DEBUG,
                 nivel_cons: int=INFO,
                 fmt: str="%(asctime)s - %(levelname)s - %(message)s",
                 fmt_fecha: str="%d-%m-%Y %I:%M:%S %p") -> None:
        """
        Inicializa una instancia de 'AssistLogger', pero sólo si es la primera vez que se crea.
        """

        if not hasattr(self, "__inicializado"):
            super().__init__()

            # Nunca lo vamos a usar, por lo que no vale la pena declararlo tal cual,
            # el checker jode conque no tiene uso el atributo
            setattr(self, "__inicializado", True)

            self._formato: str = fmt
            self._fmt_fecha: str = fmt_fecha

            self._formateador = Formatter(fmt=self.formato, datefmt=self.fmt_fecha)

            self.handler_archivo = FileHandler(filename=LOG_PATH, encoding="utf-8")
            self.handler_archivo.setLevel(nivel_arch)
            self.handler_consola = StreamHandler()
            self.handler_consola.setLevel(nivel_cons)
            self.actualizar_formateador()

            self.logger: "Logger" = getLogger(nombre_log)
            # El más bajo funcionalmente, para que no tape los handlers
            self.logger.setLevel(DEBUG)
            self.logger.addHandler(self.handler_archivo)
            self.logger.addHandler(self.handler_consola)


    def actualizar_formateador(self) -> None:
        """
        Actualiza el formateador para cada handler que el logger tiene.
        """

        self.handler_archivo.setFormatter(self.formateador)
        self.handler_consola.setFormatter(self.formateador)


    @property
    def formateador(self) -> Formatter:
        """
        Devuelve el formateador en uso.
        """

        return self._formateador

    @formateador.setter
    def formateador(self, nuevo_formateador: Formatter) -> None:

        self._formateador = nuevo_formateador
        self.actualizar_formateador()


    @property
    def formato(self) -> str:
        """
        Devuelve el formato de los mensajes del log.
        """

        return self._formato


    @formato.setter
    def formato(self, nuevo_formato) -> None:

        self._formato = nuevo_formato
        self.formateador = Formatter(fmt=self.formato, datefmt=self.fmt_fecha)


    @property
    def fmt_fecha(self) -> str:
        """
        Devuelve el formato de fecha de los mensajes del log.
        """

        return self._fmt_fecha


    @fmt_fecha.setter
    def fmt_fecha(self, nuevo_fmt_fecha: str) -> None:

        self._fmt_fecha = nuevo_fmt_fecha
        self.formateador = Formatter(fmt=self.formato, datefmt=self.fmt_fecha)


    def debug(self, mensaje: str, *args, **kwargs) -> None:
        """
        Registra un evento de nivel DEBUG.
        """

        self.logger.debug(mensaje, *args, **kwargs)


    def info(self, mensaje: str, *args, **kwargs) -> None:
        """
        Registra un evento de nivel INFO.
        """

        self.logger.info(mensaje, *args, **kwargs)


    def warning(self, mensaje: str, *args, **kwargs) -> None:
        """
        Registra un evento de nivel WARNING.
        """

        self.logger.warning(mensaje, *args, **kwargs)


    def error(self, mensaje: str, *args, **kwargs) -> None:
        """
        Registra un evento de nivel ERROR.
        """

        self.logger.error(mensaje, *args, **kwargs)


    def critical(self, message: str, *args, **kwargs) -> None:
        """
        Registra un evento de nivel CRITICAL.
        """

        self.logger.critical(message, *args, **kwargs)


    def exception(self, mensaje, *args, exc_info=True, **kwargs) -> None:
        """
        Registra una excepción.
        """

        self.logger.exception(mensaje, *args, exc_info, **kwargs)
