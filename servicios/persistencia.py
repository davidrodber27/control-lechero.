
from modelos.vaca import Vaca
from servicios.fechas import normalizar_fecha


def cargar_vacas(supabase, finca, cargar_historial=True):
    """
    Carga las vacas desde Supabase.
    El historial de producción se carga únicamente
    cuando cargar_historial=True.
    """

    respuesta_vacas = (
        supabase
        .table("vacas")
        .select("*")
        .execute()
    )

    # Solo el administrador consulta el historial.
    produccion_por_vaca = {}

    if cargar_historial:

        respuesta_produccion = (
            supabase
            .table("produccion")
            .select("*")
            .execute()
        )

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
            identificacion=datos["identificacion"],
            fecha_ultimo_parto=datos.get("fecha_ultimo_parto"),
            numero_partos=datos.get("numero_partos", 0)
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
    orden,
    litros,
    potrero
):
    """
    Registra un ordeño individual mediante la función SQL
    registrar_ordenio de Supabase.

    Si ya existe un registro para esa vaca y fecha,
    actualiza únicamente el ordeño seleccionado.
    """

    fecha_normalizada = normalizar_fecha(fecha).isoformat()

    orden_normalizada = orden.strip().lower()

    if orden_normalizada not in ("manana", "tarde"):
        raise ValueError(
            "El ordeño debe ser 'manana' o 'tarde'."
        )

    datos = {
        "p_identificacion": identificacion.strip().upper(),
        "p_fecha": fecha_normalizada,
        "p_orden": orden_normalizada,
        "p_litros": int(litros),
        "p_potrero": int(potrero)
    }

    respuesta = (
        supabase
        .rpc("registrar_ordenio", datos)
        .execute()
    )

    return respuesta.data

