
from datetime import date, datetime


def normalizar_fecha(fecha):
    """
    Convierte una fecha válida en un objeto datetime.date.

    Acepta:
    - Un objeto date.
    - Un objeto datetime.
    - Una cadena en formato AAAA-MM-DD.
    - Una cadena en formato DD/MM/AAAA.
    """

    if isinstance(fecha, datetime):
        return fecha.date()

    if isinstance(fecha, date):
        return fecha

    if isinstance(fecha, str):
        formatos = ("%Y-%m-%d", "%d/%m/%Y")

        for formato in formatos:
            try:
                return datetime.strptime(
                    fecha.strip(),
                    formato
                ).date()
            except ValueError:
                continue

    raise ValueError(
        "Fecha inválida. Usa AAAA-MM-DD o DD/MM/AAAA."
    )
