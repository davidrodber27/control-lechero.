
from modelos.vaca import Vaca
from modelos.control_lechero import ControlLechero


def cargar_vacas(supabase, finca):
    """
    Carga las vacas registradas en Supabase
    y las incorpora al objeto ControlLechero.
    """

    respuesta = (
        supabase
        .table("vacas")
        .select("*")
        .execute()
    )

    for datos in respuesta.data:
        nueva_vaca = Vaca(
            nombre=datos["nombre"],
            fecha_nacimiento=datos["fecha_nacimiento"],
            raza=datos["raza"],
            identificacion=datos["identificacion"]
        )

        finca.agregar_vaca(nueva_vaca)

    return finca

