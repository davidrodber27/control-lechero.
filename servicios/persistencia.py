

from modelos.vaca import Vaca
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

    # Agrupar la producción por identificación de vaca.
    produccion_por_vaca = {}

    for registro in respuesta_produccion.data:
        identificacion = registro["identificacion_vaca"]

        if identificacion not in produccion_por_vaca:
            produccion_por_vaca[identificacion] = []

        produccion_por_vaca[identificacion].append(registro)

    # Reconstruir cada objeto Vaca.
    for datos in respuesta_vacas.data:
        nueva_vaca = Vaca(
            nombre=datos["nombre"],
            fecha_nacimiento=datos["fecha_nacimiento"],
            raza=datos["raza"],
            identificacion=datos["identificacion"]
        )

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


def guardar_produccion(
    supabase,
    identificacion,
    fecha,
    litros_manana,
    litros_tarde,
    potrero
):
    """
    Guarda un registro diario de producción en Supabase.
    """

    fecha_normalizada = normalizar_fecha(fecha).isoformat()

    datos = {
        "identificacion_vaca": identificacion.strip().upper(),
        "fecha": fecha_normalizada,
        "litros_manana": litros_manana,
        "litros_tarde": litros_tarde,
        "potrero": potrero
    }

    respuesta = (
        supabase
        .table("produccion")
        .insert(datos)
        .execute()
    )

    return respuesta.data
