
from datetime import date, datetime

from servicios.fechas import normalizar_fecha


class Vaca:
    """
    Representa una vaca de la finca y su historial de producción.
    """

    def __init__(
        self,
        nombre: str,
        fecha_nacimiento: str,
        raza: str,
        identificacion: str | None = None
    ):
        # 1. Validar el nombre
        if not isinstance(nombre, str) or not nombre.strip():
            raise ValueError("El nombre de la vaca no puede estar vacío.")

        # 2. Validar la raza
        if not isinstance(raza, str) or not raza.strip():
            raise ValueError("La raza no puede estar vacía.")

        # 3. Validar y normalizar la identificación
        if identificacion is None:
            identificacion = nombre.strip()

        if (
            not isinstance(identificacion, str)
            or not identificacion.strip()
        ):
            raise ValueError(
                "La identificación de la vaca no puede estar vacía."
            )

        self.identificacion = identificacion.strip().upper()
        self.nombre = nombre.strip().title()
        self.raza = raza.strip().title()

        # 4. Normalizar la fecha y guardarla en formato ISO
        fecha_normalizada = normalizar_fecha(fecha_nacimiento)

        if isinstance(fecha_normalizada, datetime):
            fecha_normalizada = fecha_normalizada.date()

        if isinstance(fecha_normalizada, date):
            fecha_normalizada = fecha_normalizada.isoformat()

        self.fecha_nacimiento = fecha_normalizada

        fecha_nac = date.fromisoformat(self.fecha_nacimiento)

        if fecha_nac > date.today():
            raise ValueError(
                "La fecha de nacimiento no puede estar en el futuro."
            )

        # Clave: fecha ISO. Valor: producción y potrero de ese día.
        self.registros = {}

    @property
    def edad_actual(self) -> str:
        """Calcula la edad actual en años y meses completos."""

        fecha_nac = date.fromisoformat(self.fecha_nacimiento)
        hoy = date.today()

        anos = hoy.year - fecha_nac.year
        meses = hoy.month - fecha_nac.month

        if hoy.day < fecha_nac.day:
            meses -= 1

        if meses < 0:
            anos -= 1
            meses += 12

        return f"{anos} años y {meses} meses"

    @staticmethod
    def validar_litros(litros):
        """Acepta únicamente litros enteros no negativos."""

        if type(litros) is not int:
            raise TypeError("Los litros deben ser números enteros.")

        if litros < 0:
            raise ValueError("Los litros no pueden ser negativos.")

    def registrar_produccion(
        self,
        fecha,
        litros_manana: int,
        litros_tarde: int,
        potrero: int
    ):
        """Registra la producción de ambos ordeños para una fecha."""

        fecha_normalizada = normalizar_fecha(fecha)

        if isinstance(fecha_normalizada, date):
            fecha_normalizada = fecha_normalizada.isoformat()

        if date.fromisoformat(fecha_normalizada) > date.today():
            raise ValueError(
                "La fecha de producción no puede estar en el futuro."
            )

        self.validar_litros(litros_manana)
        self.validar_litros(litros_tarde)

        if type(potrero) is not int or not 1 <= potrero <= 12:
            raise ValueError(
                "El potrero debe ser un número entero entre 1 y 12."
            )

        if fecha_normalizada in self.registros:
            return False

        self.registros[fecha_normalizada] = {
            "litros_manana": litros_manana,
            "litros_tarde": litros_tarde,
            "potrero": potrero
        }

        return True

    def calcular_produccion(self, fecha):
        """Devuelve los litros del día o None si no hay registro."""

        fecha_normalizada = normalizar_fecha(fecha)

        if isinstance(fecha_normalizada, date):
            fecha_normalizada = fecha_normalizada.isoformat()

        registro = self.registros.get(fecha_normalizada)

        if registro is None:
            return None

        return (
            registro["litros_manana"]
            + registro["litros_tarde"]
        )

    def produccion_acumulada(self) -> int:
        """Suma la producción de todos los días registrados."""

        return sum(
            registro["litros_manana"] + registro["litros_tarde"]
            for registro in self.registros.values()
        )

    def __repr__(self) -> str:
        return (
            f"Vaca: {self.nombre} | "
            f"ID: {self.identificacion} | "
            f"Raza: {self.raza} | "
            f"Edad: {self.edad_actual} | "
            f"Producción acumulada: {self.produccion_acumulada()} L"
        )
