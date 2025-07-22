"""
Módulo para atajos de operaciones sobre permisos de comandos.
"""

from typing import TYPE_CHECKING, Optional, TypeAlias

from ..database import (
    actualizar_dato_de_tabla,
    borrar_datos_de_tabla,
    insertar_datos_en_tabla,
    sacar_datos_de_tabla,
)
from ..enums import NivelPermisos

if TYPE_CHECKING:
    from ..database import DictConds

UserIDs: TypeAlias = tuple[int, ...]
RoleIDs: TypeAlias = tuple[int, ...]
Perms: TypeAlias = tuple[UserIDs, RoleIDs]

PERMISOS_IDS: str = "op_list"
"Nombre de la tabla de permisos por usuario en la DB."

PERMISOS_ROLES: str = "op_roles"
"Nombre de la tabla de permisos por rol en la DB."


def _get_admins(*, conds_usuarios: "DictConds", conds_roles: "DictConds") -> Perms:
    """
    Intenta buscar todos los administradores con privilegios según condiciones dadas.
    """

    id_usuarios = []
    id_roles = []

    res_usuarios = sacar_datos_de_tabla(PERMISOS_IDS,
                                        sacar_uno=False,
                                        **conds_usuarios)

    res_roles = sacar_datos_de_tabla(PERMISOS_ROLES,
                                     sacar_uno=False,
                                     **conds_roles)

    # Los IDs son siempre la segunda columna
    id_usuarios = tuple(u[1] for u in res_usuarios)
    id_roles = tuple(r[1] for r in res_roles)

    return id_usuarios, id_roles


def _perms_dict(perms_lvl: NivelPermisos, por_lo_menos: bool=True) -> "DictConds":
    """
    Crea un diccionario personalizado para las condiciones de consulta
    de permisos en la DB.
    """

    if por_lo_menos:
        # 'where' es una clave especial en estos diccionarios
        return dict(where=(f"op_level <= {perms_lvl.value}",))

    return dict(op_level=perms_lvl)


def get_admins_por_guild(guild_id: int) -> Perms:
    """
    Intenta buscar todos los administradores con privilegios según
    el ID de un guild dado.
    """

    return _get_admins(conds_usuarios=dict(allowed_in=guild_id),
                       conds_roles=dict(used_in=guild_id))


def get_admins_por_nivel(perms_lvl: NivelPermisos, *, por_lo_menos: bool=True) -> Perms:
    """
    Intenta buscar todos los administradores con privilegios según
    el ID de un guild dado.

    Si 'por_lo_menos' es especificado como `True`, se busca que el nivel de permisos sea mayor
    o igual al especificado, no exactamente igual.
    """

    permisos_conds = _perms_dict(perms_lvl, por_lo_menos)

    return _get_admins(conds_usuarios=permisos_conds,
                       conds_roles=permisos_conds)



def get_admins_por_nivel_y_guild(perms_lvl: NivelPermisos,
                                 guild_id: Optional[int]=None,
                                 *,
                                 por_lo_menos: bool=True) -> Perms:
    """
    Intenta buscar todos los administradores con privilegios según
    el nivel de permisos y el ID de un guild dados.

    Si 'por_lo_menos' es especificado como `True`, se busca que el nivel de permisos sea mayor
    o igual al especificado, no exactamente igual.
    """

    permisos_conds_usuarios = _perms_dict(perms_lvl, por_lo_menos)
    permisos_conds_roles = permisos_conds_usuarios.copy()

    permisos_conds_usuarios.update(allowed_in=guild_id)
    permisos_conds_roles.update(used_in=guild_id)

    return _get_admins(conds_usuarios=permisos_conds_usuarios,
                       conds_roles=permisos_conds_roles)


def op_usuario(id_usuario: int, nivel: NivelPermisos, guild_id: int) -> Optional[NivelPermisos]:
    """
    Intenta actualizar el nivel de permisos que un usuario dado tiene en el guild seleccionado,
    insertando datos por primera vez si hace falta.

    Devuelve el nivel anterior de permisos que el usuario tenía, o `None` si no existía todavía
    en la tabla.
    """

    res_usuario = sacar_datos_de_tabla(PERMISOS_IDS,
                                       sacar_uno=True,
                                       user_id=id_usuario,
                                       allowed_in=guild_id)

    if res_usuario:
        actualizar_dato_de_tabla(PERMISOS_IDS,
                                 nombre_col="op_level",
                                 valor=nivel.value)
        return NivelPermisos(res_usuario[2])

    insertar_datos_en_tabla(PERMISOS_IDS,
                            llave_primaria_por_defecto=True,
                            valores=(id_usuario, nivel.value, guild_id))
    return None


def deop_usuario(id_usuario: int, guild_id: int) -> Optional[NivelPermisos]:
    """
    Intenta eliminar un usuario de la tabla de permisos relevante.

    Devuelve el nivel de permisos que el usuario tenía, o `None` si dicho usuario no existe
    en la tabla.
    """

    res_usuario = sacar_datos_de_tabla(PERMISOS_IDS,
                                       sacar_uno=True,
                                       user_id=id_usuario,
                                       allowed_in=guild_id)

    if not res_usuario:
        return None

    borrar_datos_de_tabla(PERMISOS_IDS, user_id=id_usuario, allowed_in=guild_id)
    return NivelPermisos(res_usuario[2])


def op_rol(id_rol: int, nivel: NivelPermisos, guild_id: int) -> Optional[NivelPermisos]:
    """
    Intenta actualizar el nivel de permisos que un rol dado tiene en el guild seleccionado,
    insertando datos por primera vez si hace falta.

    Devuelve el nivel anterior de permisos que el rol tenía, o `None` si no existía todavía
    en la tabla.
    """

    res_rol = sacar_datos_de_tabla(PERMISOS_ROLES,
                                   sacar_uno=True,
                                   user_id=id_rol,
                                   used_in=guild_id)

    if res_rol:
        actualizar_dato_de_tabla(PERMISOS_ROLES,
                                 nombre_col="op_level",
                                 valor=nivel.value)
        return NivelPermisos(res_rol[2])

    insertar_datos_en_tabla(PERMISOS_ROLES,
                            llave_primaria_por_defecto=True,
                            valores=(id_rol, nivel.value, guild_id))
    return None


def deop_rol(id_rol: int, guild_id: int) -> Optional[NivelPermisos]:
    """
    Intenta eliminar un rol de la tabla de permisos relevante.

    Devuelve el nivel de permisos que el rol tenía, o `None` si dicho rol no existe
    en la tabla.
    """

    res_rol = sacar_datos_de_tabla(PERMISOS_IDS,
                                   sacar_uno=True,
                                   user_id=id_rol,
                                   allowed_in=guild_id)

    if not res_rol:
        return None

    borrar_datos_de_tabla(PERMISOS_IDS, user_id=id_rol, allowed_in=guild_id)
    return NivelPermisos(res_rol[2])
