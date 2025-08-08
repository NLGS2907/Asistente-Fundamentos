"Módulo para atajos de operaciones sobre permisos de comandos."

from typing import TYPE_CHECKING, Optional, TypeAlias, Iterable

from ..database import (
    actualizar_dato_de_tabla,
    borrar_datos_de_tabla,
    insertar_datos_en_tabla,
    sacar_datos_de_tabla,
)
from ..enums import NivelPermisos

if TYPE_CHECKING:
    from ..database import DictConds

UserIDs: TypeAlias = dict[int, int]
RoleIDs: TypeAlias = dict[int, int]
Perms: TypeAlias = tuple[UserIDs, RoleIDs]

PERMISOS_IDS: str = "op_list"
"Nombre de la tabla de permisos por usuario en la DB."

PERMISOS_ROLES: str = "op_roles"
"Nombre de la tabla de permisos por rol en la DB."


def _get_admins(*, conds_usuarios: "DictConds", conds_roles: "DictConds") -> Perms:
    "Intenta buscar todos los administradores con privilegios según condiciones dadas."

    res_usuarios = sacar_datos_de_tabla(PERMISOS_IDS,
                                        sacar_uno=False,
                                        **conds_usuarios)

    res_roles = sacar_datos_de_tabla(PERMISOS_ROLES,
                                     sacar_uno=False,
                                     **conds_roles)

    # Los IDs son siempre la segunda columna
    id_usuarios = {u[1]: u[2] for u in res_usuarios}
    id_roles = {r[1]: r[2] for r in res_roles}

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
                                 guild_id: int,
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


def get_nivel_de_admin(user_id: int,
                       roles: Iterable[int],
                       guild_id: int,
                       *,
                       ignorar_usuarios: bool=False,
                       ignorar_roles: bool=False) -> Optional[NivelPermisos]:
    """
    Consigue el nivel de permisos de un usuario en particular en un guild dado.
    Devuelve `None` si el usuario no tiene permisos.

    El permiso individual tiene precedencia: si el usuario pertenece a un rol con rol
    `ADMINISTRADOR`, pero el usuario en sí tiene permiso individual `MODERADOR`, esta función
    devolverá `MODERADOR`.
    Dicho eso, hay opciones para ignorar uno u otro, pero si se ignoran ambos se garantiza que
    el resultado sea `None`.
    """

    id_usuarios, id_roles = _get_admins(conds_usuarios=dict(allowed_in=guild_id),
                                        conds_roles=dict(used_in=guild_id))

    # El usuario tiene un permiso individual
    if not ignorar_usuarios and user_id in id_usuarios:
        return NivelPermisos(id_usuarios[user_id])

    nivel_permiso = None
    if not ignorar_roles:
        # Si el usuario pertenece a un rol con permiso, devolver el permiso más privilegiado.
        for rol, nivel in id_roles.items():
            if rol in roles:
                if nivel_permiso is None or nivel_permiso < nivel:
                    nivel_permiso = nivel

        if nivel_permiso is not None:
            return NivelPermisos(nivel_permiso)

    return nivel_permiso  # a este punto es None


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
                                 valor=nivel.value,
                                 user_id=id_usuario,
                                 allowed_in=guild_id)
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
                                   role_id=id_rol,
                                   used_in=guild_id)

    if res_rol:
        actualizar_dato_de_tabla(PERMISOS_ROLES,
                                 nombre_col="op_level",
                                 valor=nivel.value,
                                 role_id=id_rol,
                                 used_in=guild_id)
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

    res_rol = sacar_datos_de_tabla(PERMISOS_ROLES,
                                   sacar_uno=True,
                                   role_id=id_rol,
                                   used_in=guild_id)

    if not res_rol:
        return None

    borrar_datos_de_tabla(PERMISOS_ROLES, role_id=id_rol, used_in=guild_id)
    return NivelPermisos(res_rol[2])
