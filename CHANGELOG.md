# Changelog

Historial con detalles de cambios entre versiones del asistente.

|                  |                  |                  |                  |      Version     |
|:----------------:|:----------------:|:----------------:|:----------------:|:----------------:|
|                  |                  |  [2.0.1](#v201)  |  [2.0.2](#v202)  |**[2.0.3](#v203)**|
|                  |                  |                  |  [1.4.1](#v141)  |**[2.0.0](#v200)**|
|                  |                  |                  |                  |**[1.4.0](#v140)**|
|                  |                  |                  |  [1.2.1](#v121)  |**[1.3.0](#v130)**|
|                  |                  |                  |                  |**[1.2.0](#v120)**|
|  [1.0.1](#v101)  |  [1.0.2](#v102)  |  [1.0.3](#v103)  |  [1.0.4](#v104)  |**[1.1.0](#v110)**|
|                  |                  |                  |                  |**[1.0.0](#v100)**|

<hr/>

### v2.0.3

* **Mejorado el _workflow_ de _releases_:** Ahora debería tener notas personalizadas que refieren a este _changelog_.
* `/inscribirse` pasa a llamarse `/roles`.
* **Modularizada la lógica de sesión HTTP y de Cogs.** Entre otras cosas, cambiar mensajes de error.
* _Varios bugfixes._

<hr style="height:2px" />

### v2.0.2

* **Actualizadas las dependencias.**
  - `discord.py` (2.5.2 → **2.6.0**)
  - Se agregó `aiohttp` (**3.12.15**)
* **Agregado grupo de comandos `/log`**.
  - `/log get`
  - `/log tail`
  - `/log flush`
* **Agregada sesión asincrónica** para poder hacer _requests_ HTTP.
* Nuevo comando `/inscribirse` para recibir roles en el servidor de Fundamentos de Programación.

<hr style="height:2px" />

### v2.0.1

* _fixes_ para bugs de parámetros de búsqueda en `/random`

<hr style="height:2px" />

## v2.0.0

* **El bot ahora se llama *"Asistente de Fundamentos"*, ya no *"Lector de Ejercicios"***. Esto es para ser más conforme con futuras características.
* **¡Nuevo logo!** Los _assets_ de versiones anteriores todavía se encuentran bajo el nombre de [v1](./img/logo/v1/).
* Cambiados los estilos de nombre de guías de `1c2024` a `2024C1`.
* **Actualizada la versión de la guía** a la revisión del 7 de Marzo de 2024, bajo la denominación `2024C1`.
  - Ediciones en el enunciado del ejercicio **11.2**.
  - El enunciado del ejercicio **11.6** fue reemplazado por otro completamente distinto.
  - Nuevo ejercicios **11.7** y **11.8**.
  - El enunciado del ejercicio **17.11** fue reemplazado por otro diferente.
  - Nuevos ejercicios del **17.12** al **17.18**.
* **Actualizadas las dependencias.**
  - discord.py (2.2.2 → **2.5.2**)
  - python-dotenv **fue eliminada**.
* Remodularizados los módulos `main` y `tests` del proyecto. Ahora están como carpetas aparte en el directorio raíz.
  - `main` ahora se llama `asistente`, para ser consistente con la nueva forma de invocar al bot.
* Limpiada toda mención de los "prefijos". Ahora el bot usa exclusivamente _app commands_ con `/`.
* Mejores mensajes de error para los Cogs de comandos.
* **La base de datos ya no se sube.** Ahora se crea sola y es única para cada instancia del bot.
  - Hace uso de un _script_ inicial para poblarse sola con las tablas necesarias.
* **Mejoras al Logger:**
  - Ahora sigue un patrón _Singleton_, por lo que se puede instanciar en cualquier parte del proyecto sin miedo a guardar el mismo registro varias veces.
  - Distintos niveles de logueo de registros para la consola y para el archivo.
  - Ahora el asistente se puede ejecutar con los argumentos `-v` o `--verbose` para guardar registros en consola con el nivel `DEBUG`.
  - Ahora también guarda registros del _traceback_ de `discord.py`, no sólo los del asistente.
* `/version` fue eliminado, y su funcionalidad quedó incluida en el comando `/info`.
* El _workflow_ para GitHub de PyLint fue cambiado por el de Ruff.
* `/reboot` y `/shutdown` ahora sólo están disponibles para el dueño de la aplicación ~~(yo)~~. Sino es un riesgo de seguridad importante.
* Se agregaron algunos secciones extra en el [README](./README.md).
  - Explicación simple de los comandos más comunes.
  - Un caso de uso para `/ej`.
* **Remodelado el comando `/ej`:**
  - Ahora todo ocurre en mensajes "efímeros" de Discord, con la posibilidad de todavía "imprimir" el mensaje en el canal con un nuevo botón.
  - Incluidos algunos fixes para que `/ej` _(así como comandos similares)_ puedan funcionar en canales privados o DMs.


<hr style="height:4px" />

### v1.4.1

* **Actualizadas las dependencias.**
  - discord.py (2.1.0 → **2.2.2**)
  - python-dotenv (0.2.1 → **1.0.0**)

* **Uso de `typing.Union` en vez de `|`** para un poco retrocompatibilidad.

<hr style="height:2px" />

## v1.4.0

* Arreglados bugs con el menu de `/ej`, en donde el menu de unidades no funcionaba para las unidades `2` y `12`.
* **Actualizada la versión de la guía.** Ahora utiliza la revisión del 6 de Marzo de 2022 bajo el nombre `1c2022`.
  - Cambiada *una* palabra del ejercicio **1.6.b)**.
  - Expandido el enunciado del ejercicio **7.11**.
  - Nuevo ejercicio **7.13**.
* **Comando `/meme` removido.** Cayó en desuso y no era rentable mantener las claves.
* **Comandos `/whatsnew` y `/rps` removidos.**
* **Mejorada la lógica de archivos.** Ahora usan búsqueda recursiva e instancias de la clase `pathlib.Path`, en vez de las funciones de `os.path`.
* **Ahora se usa una DB de SQLite3,** en vez de un módulo de constantes.

<hr style="height:4px" />

## v1.3.0

* Puesto que [discord.py](https://github.com/Rapptz/discord.py) ha continuado su mantenimiento, y las *features* que promete traer son preferidas, **se ha decidido en buena fe volver a usar esta librería.**

* **Agregados los *slash commands*.**

* **Agregado nuevo comando `reboot`.** Ahora se puede reiniciar el bot sin tener que apagarlo manualmente.

<hr style="height:4px" />

### v1.2.1

* **Simplificados algunos imports en las pruebas y en el main.** No deberían tener nombres redundantes.
* **Agregados scripts ejecutables.** Ahora debería ser más intuitivo correr el bot.

<hr style="height:2px" />

## v1.2.0

* **Migración a Pycord.** La librería que se venía usando, [discord.py](https://github.com/Rapptz/discord.py), cesó su mantenimiento, y por lo
tanto el bot migró a usar [pycord](https://github.com/Pycord-Development/pycord), un *fork* de discord.py casi idéntico y más actualizado.

* **Reformados los comandos.** Ahora hace uso de `Cogs` para mejor organización de los mismos.

* **Modularización.** Siguiendo la mejora de solidez técnica descrita arriba, muchas funciones
y clases fueron separadas en sus propios módulos.

* **Algunos Comandos ahora usan `Embeds`.** Esto permite una presentación más prolija.

<hr style="height:4px" />

## v1.1.0

Esta versión introduce una nueva imagen para el bot, manejo de imágenes por
Imgur, para mejor experiencia de memes. También se introducen menús contextuales para `ej` y `guia`.

* **¡Nuevo Logo!** Las referencias se encuentran en la carpeta de [imágenes](img).

* **Hace uso de [`imgur-python`](https://pypi.org/project/imgur-python/)** para manejar imágenes a través del bot de Discord.

* **Nuevo Archivo `cliente_imgur.py`** para guardar la lógica de la
aplicación que representa el cliente de Imgur.

* **Ahora el comando `meme` ya no acepta ids de links.** Sin embargo, ahora
acepta que se le pase el índice de meme si se quiere uno en concreto de la
colección en Imgur.

* **Nuevo parámetro `add` para el comando `meme`**. Con esto, si el mensaje que envía el comando refiere a una imagen, se agrega esta a la colección de memes.

* **Nuevo Archivo `interfaces.py`** en donde guardar las interfaces usadas
en los mensajes del bot.

* **Ahora `guia` tiene un menú contextual.** Permite seleccionar más
intuitivamente las versiones de la guía, y se llama con `guia` sin
parámetros.

* **Similarmente con `ej`,** ahora este tiene no sólo también un menú
selector, si no también hace uso de botones para navegar por los ejercicios.

* **Agregado banco entero de palabras en español para el ahorcado.** Ahora
hay `80946` combinaciones posibles. Unas pocas más.

* **El bot ahora es más** ¿...competitivo?

<hr style="height:4px" />

### v1.0.4

Esta versión tiene más que nada mantenimiento y mejoras internas:

* **Mejorada la forma de registrar eventos.** Ahora hace uso del módulo `logging` para registrar eventos en la ejecución del bot.

* **Nuevo archivo** `lector.log` para guardar dichos registros.

<hr style="height:2px" />

### v1.0.3

* **Agregado una actividad `!info`** en el estado del bot.

* **Agregados nuevos mensajes de error** para excepciones del comando `ej`.

<hr style="height:2px" />

### v1.0.2

* **Mejorado un poco el código.** Ahora el cuerpo del código sigue mejor las convenciones de python.
* **Agregadas** algunas que otras palabras nuevas que pueden tocar en el ahorcado.

<hr style="height:2px" />

### v1.0.1

* **Agregado comando `clear`** para limpiar mensajes del bot.

<hr style="height:4px" />

## v1.0.0

* Ahora el bot proviene de una clase `CustomBot` que sobrecarga a la clase de Discord `commands.Bot`. Esto es para contener información persistente, pero los
  comandos siguen siendo definidos mediante decoradores.

* Mejoradas las *type hints* de varias funciones y la documentación en general.

* La estructura del lector de la guía es más flexible y configurable y no depende de valores *hardcodeados* como antes.

* **Nuevo comando `prefix`** con el que cambiar el prefijo del comando. Puede configurarse por separado para cada servidor.

* **Nuevo comando `guia`** con el que configurar la revisión de la guía de ejercicios a utilizar (por defecto actualmente se utiliza la versión `2c2019`).
  De nuevo, la configuración de cada servidor es independiente de las otras. Por ahora la única versión disponible es `2c2019`, pero añadido está el soporte para
  futuras revisiones de la guía.

* Ahora el comando `info` muestra también la versión de la guía.

* **Aún más** memes. *Muuuchos más*.

* **¡Introducido el juego 'hanged' (ahorcado)!**. Se invoca mediante el nuevo comando `hanged` o su alias `ahorcado`. Hace uso de los nuevos hilos en Discord, 
  introducidos en la API 2.0.

* El juego de ahorcado tiene su propia clase, en un archivo separado, y los datos de las partidas se mantienen dentro de la clase `CustomBot`. Hace uso de un
  archivo `.txt` separado para generar las palabras.

* `meme` ahora soporta también que se le pase el ID del meme, por si se quiere uno en concreto (aunque no funciona si el link no comienza con `https://i.imgur.com`)