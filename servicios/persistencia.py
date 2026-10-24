

from modelos.vaca import Vaca
from modelos.control_lechero import ControlLechero
from servicios.fechas import normalizar_fecha


def cargar_vacas(supabase, finca):
    """
    Carga las vacas y su historial de producción
    desde Supabase al objeto ControlLechero.
    """

    respuesta_vacas = (
        supabase
        .table("vacas")
        .select("*")
        .execute()
    )

    respuesta_produccion = (
        supabase
        .table("produccion")
        .select("*")
        .execute()
    )

    # Crear un diccionario temporal para asociar
    # cada registro con la identificación de su vaca.
    produccion_por_vaca = {}

    for registro in respuesta_produccion.data:
        identificacion = registro["identificacion_vaca"]

        if identificacion not in produccion_por_vaca:
            produccion_por_vaca[identificacion] = []

        produccion_por_vaca[identificacion].append(registro)

    # Reconstruir los objetos Vaca.
    for datos in respuesta_vacas.data:
        nueva_vaca = Vaca(
            nombre=datos["nombre"],
            fecha_nacimiento=datos["fecha_nacimiento"],
            raza=datos["raza"],
            identificacion=datos["identificacion"]
        )

        # Cargar los registros diarios de esa vaca.
        registros = produccion_por_vaca.get(
            nueva_vaca.identificacion,
            []
        )

        for registro in registros:
            nueva_vaca.registrar_produccion(
                fecha=normalizar_fecha(registro["fecha"]),
                litros_manana=registro["litros_manana"],
                litros_tarde=registro["litros_tarde"],
                potrero=registro["potrero"]
            )

        finca.agregar_vaca(nueva_vaca)

    return finca
