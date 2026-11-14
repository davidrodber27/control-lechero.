
import streamlit as st
from datetime import date

from servicios.persistencia import consultar_produccion_hoy


def mostrar_reporte_diario(finca, supabase, rol):

    st.divider()
    st.header("Reporte diario de producción")

    # --------------------------------------------------
    # REPORTE DEL EMPLEADO: SOLAMENTE EL DÍA ACTUAL
    # --------------------------------------------------

    if rol == "empleado":

        st.info("Estás consultando exclusivamente la producción de hoy.")

        try:
            registros = consultar_produccion_hoy(supabase)

        except Exception as error:
            st.error("No fue posible consultar la producción de hoy.")
            st.code(str(error))
            return

        if not registros:
            st.info("Todavía no hay producción registrada para hoy.")
            return

        produccion_total = sum(
            (registro["litros_manana"] or 0)
            + (registro["litros_tarde"] or 0)
            for registro in registros
        )

        col1, col2 = st.columns(2)

        with col1:
            st.metric(
                "Producción total del día",
                f"{produccion_total} L"
            )

        with col2:
            st.metric(
                "Vacas con producción registrada",
                len(registros)
            )

        datos_vacas = []

        for registro in registros:

            litros_manana = registro["litros_manana"]
            litros_tarde = registro["litros_tarde"]

            total_vaca = (
                (litros_manana or 0)
                + (litros_tarde or 0)
            )

            datos_vacas.append({
                "Identificación": registro["identificacion_vaca"],
                "Vaca": registro["nombre_vaca"],
                "Mañana (L)": (
                    litros_manana
                    if litros_manana is not None
                    else "Pendiente"
                ),
                "Tarde (L)": (
                    litros_tarde
                    if litros_tarde is not None
                    else "Pendiente"
                ),
                "Total (L)": total_vaca,
                "Potrero": registro["potrero"]
            })

        st.subheader("Producción por vaca")

        st.dataframe(
            datos_vacas,
            use_container_width=True,
            hide_index=True
        )

        # Producción agrupada por potrero.
        st.subheader("Producción por potrero")

        produccion_potreros = {}

        for registro in registros:

            potrero = registro["potrero"]

            litros = (
                (registro["litros_manana"] or 0)
                + (registro["litros_tarde"] or 0)
            )

            produccion_potreros[potrero] = (
                produccion_potreros.get(potrero, 0) + litros
            )

        datos_potreros = [
            {
                "Potrero": potrero,
                "Producción (L)": litros
            }
            for potrero, litros in sorted(
                produccion_potreros.items()
            )
        ]

        st.dataframe(
            datos_potreros,
            use_container_width=True,
            hide_index=True
        )

        return

    # --------------------------------------------------
    # REPORTE DEL ADMINISTRADOR: FECHA SELECCIONABLE
    # --------------------------------------------------

    fecha_reporte = st.date_input(
        "Selecciona la fecha que deseas consultar",
        value=date.today(),
        max_value=date.today(),
        key="fecha_reporte"
    )

    produccion_total = finca.produccion_total(fecha_reporte)

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Producción total del día",
            f"{produccion_total} L"
        )

    with col2:
        registros_dia = sum(
            1
            for vaca in finca.vacas.values()
            if fecha_reporte.isoformat() in vaca.registros
        )

        st.metric(
            "Vacas con producción registrada",
            registros_dia
        )

    datos_vacas = []

    for vaca in finca.vacas.values():

        registro = vaca.registros.get(
            fecha_reporte.isoformat()
        )

        if registro is not None:

            litros_manana = registro["litros_manana"]
            litros_tarde = registro["litros_tarde"]

            total_vaca = (
                (litros_manana or 0)
                + (litros_tarde or 0)
            )

            datos_vacas.append({
                "Identificación": vaca.identificacion,
                "Vaca": vaca.nombre,
                "Mañana (L)": (
                    litros_manana
                    if litros_manana is not None
                    else "Pendiente"
                ),
                "Tarde (L)": (
                    litros_tarde
                    if litros_tarde is not None
                    else "Pendiente"
                ),
                "Total (L)": total_vaca,
                "Potrero": registro["potrero"]
            })

    st.subheader("Producción por vaca")

    if datos_vacas:
        st.dataframe(
            datos_vacas,
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info("No hay producción registrada para esta fecha.")

    # Producción agrupada por potrero.
    st.subheader("Producción por potrero")

    produccion_potreros = finca.produccion_por_potrero(
        fecha_reporte
    )

    if produccion_potreros:

        datos_potreros = [
            {
                "Potrero": potrero,
                "Producción (L)": litros
            }
            for potrero, litros in sorted(
                produccion_potreros.items()
            )
        ]

        st.dataframe(
            datos_potreros,
            use_container_width=True,
            hide_index=True
        )

    else:
        st.info(
            "No hay producción asociada a potreros para esta fecha."
        )

