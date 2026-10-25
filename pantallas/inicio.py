
import streamlit as st
from datetime import date


def mostrar_inicio(finca):
    """Muestra el resumen principal de la finca."""

    st.title("🐄 Control Lechero")
    st.subheader("Hato La Casita")

    st.write(
        "Sistema de gestión del hato "
        "y control de producción de leche."
    )

    st.divider()

    st.header("Resumen de la finca")

    total_vacas = finca.cantidad_vacas()
    produccion_hoy = finca.produccion_total(date.today())

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Vacas registradas", total_vacas)

    with col2:
        st.metric(
            "Producción de hoy",
            f"{produccion_hoy} L"
        )

    with col3:
        st.metric("Potreros", 12)
