
from datetime import date

from modelos.vaca import Vaca
from servicios.fechas import normalizar_fecha


class ControlLechero:
    """
    Administra las vacas y la producción de la finca.
    """

    def __init__(self, nombre_finca: str):
        if not isinstance(nombre_finca, str) or not nombre_finca.strip():
            raise ValueError("El nombre de la finca no puede estar vacío.")

        self.nombre_finca = nombre_finca.strip().title()

        # Diccionario cuya clave es la identificación de cada vaca.
        self.vacas = {}

    def agregar_vaca(self, vaca: Vaca) -> bool:
        """Agrega una vaca si su identificación no está registrada."""

        if not isinstance(vaca, Vaca):
            raise TypeError("Solo se pueden agregar objetos de tipo Vaca.")

        identificacion = vaca.identificacion.casefold()

        if identificacion in self.vacas:
            return False

        self.vacas[identificacion] = vaca
        return True

    def buscar_vaca(self, identificacion: str):
        """Busca una vaca por su identificación."""

        if not isinstance(identificacion, str):
            return None

        return self.vacas.get(identificacion.strip().casefold())

    def eliminar_vaca(self, identificacion: str) -> bool:
        """Elimina una vaca por su identificación."""

        vaca = self.buscar_vaca(identificacion)

        if vaca is None:
            return False

        del self.vacas[vaca.identificacion.casefold()]
        return True

    def registrar_produccion(
        self,
        identificacion: str,
        fecha,
        litros_manana: int,
        litros_tarde: int,
        potrero: int
    ) -> bool:
        """Registra los dos ordeños de una vaca en una fecha."""

        vaca = self.buscar_vaca(identificacion)

        if vaca is None:
            raise ValueError("No existe una vaca con esa identificación.")

        return vaca.registrar_produccion(
            fecha,
            litros_manana,
            litros_tarde,
            potrero
        )


    
    def actualizar_produccion(
        self,
        identificacion: str,
        fecha,
        litros_manana: int,
        litros_tarde: int,
        potrero: int
    ) -> bool:
        """Actualiza la producción existente de una vaca."""

        vaca = self.buscar_vaca(identificacion)

        if vaca is None:
            raise ValueError(
                "No existe una vaca con esa identificación."
            )

        return vaca.actualizar_produccion(
            fecha=fecha,
            litros_manana=litros_manana,
            litros_tarde=litros_tarde,
            potrero=potrero
        )

    def produccion_total(self, fecha) -> int:
        """Suma la producción de todas las vacas en una fecha."""

        fecha_normalizada = normalizar_fecha(fecha).isoformat()

        return sum(
            vaca.calcular_produccion(fecha_normalizada) or 0
            for vaca in self.vacas.values()
        )

    def produccion_por_potrero(self, fecha) -> dict:
        """Calcula la producción diaria agrupada por potrero."""

        fecha_normalizada = normalizar_fecha(fecha).isoformat()
        produccion = {}

        for vaca in self.vacas.values():
            registro = vaca.registros.get(fecha_normalizada)

            if registro is not None:
                potrero = registro["potrero"]
                litros = (
                    registro["litros_manana"]
                    + registro["litros_tarde"]
                )

                produccion[potrero] = (
                    produccion.get(potrero, 0) + litros
                )

        return produccion

    def cantidad_vacas(self) -> int:
        """Devuelve el número de vacas registradas."""

        return len(self.vacas)
