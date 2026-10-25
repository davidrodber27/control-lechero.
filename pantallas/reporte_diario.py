
import streamlit as st
from datetime import date


def mostrar_reporte_diario(finca):

    st.divider()
    st.header("Reporte diario de producción")

    fecha_reporte = st.date_input(
        "Selecciona la fecha que deseas consultar",
        value=date.today(),
        max_value=date.today(),
        key="fecha_reporte"
    )

    produccion_total = finca.produccion_total(
        fecha_reporte
    )

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

    # Construir el detalle por vaca
    datos_vacas = []

    for vaca in finca.vacas.values():

        registro = vaca.registros.get(
            fecha_reporte.isoformat()
        )

        if registro is not None:

            total_vaca = (
                registro["litros_manana"]
                + registro["litros_tarde"]
            )

            datos_vacas.append({
                "Identificación": vaca.identificacion,
                "Vaca": vaca.nombre,
                "Mañana (L)": registro["litros_manana"],
                "Tarde (L)": registro["litros_tarde"],
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
        st.info(
            "No hay producción registrada para esta fecha."
        )

    # Producción agrupada por potrero
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
            "No hay producción asociada a potreros "
            "para esta fecha."
        )
