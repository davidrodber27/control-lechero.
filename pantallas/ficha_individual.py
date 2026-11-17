
import streamlit as st
from datetime import date


def mostrar_ficha_individual(finca):

    st.title("🐄 Ficha individual")
    st.caption(
        "Consulta la información general, reproductiva "
        "y genealógica de cada vaca."
    )

    vacas = list(finca.vacas.values())

    if not vacas:
        st.info("No hay vacas registradas en la finca.")
        return

    opciones_vacas = {
        f"{vaca.identificacion} - {vaca.nombre}": vaca
        for vaca in vacas
    }

    seleccion = st.selectbox(
        "Selecciona una vaca:",
        options=list(opciones_vacas.keys()),
        index=None,
        placeholder="Buscar por identificación o nombre..."
    )

    if seleccion is None:
        st.info("Selecciona una vaca para consultar su ficha.")
        return

    vaca = opciones_vacas[seleccion]

    st.divider()

    # DATOS GENERALES
    st.subheader("Datos generales")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Nombre", vaca.nombre)

    with col2:
        st.metric("Identificación", vaca.identificacion)

    with col3:
        st.metric("Raza", vaca.raza)

    fecha_nacimiento = date.fromisoformat(
        vaca.fecha_nacimiento
    )

    st.write(
        "**Fecha de nacimiento:**",
        fecha_nacimiento.strftime("%d/%m/%Y")
    )

    st.write("**Edad actual:**", vaca.edad_actual)

    # CONTROL REPRODUCTIVO
    st.divider()
    st.subheader("Control reproductivo")

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Número de partos", vaca.numero_partos)

    with col2:
        if vaca.fecha_ultimo_parto:
            st.metric("Días posparto", vaca.dias_posparto)
        else:
            st.metric("Días posparto", "Sin registro")

    if vaca.fecha_ultimo_parto:
        fecha_parto = date.fromisoformat(
            vaca.fecha_ultimo_parto
        )

        st.write(
            "**Último parto:**",
            fecha_parto.strftime("%d/%m/%Y")
        )
    else:
        st.info("No hay fecha del último parto registrada.")

    # ASCENDENCIA
    st.divider()
    st.subheader("Ascendencia")

    col_madre, col_padre = st.columns(2)

    with col_madre:
        st.markdown("### Madre")
        st.write("**Nombre:**", vaca.madre_nombre or "No registrado")
        st.write("**Raza:**", vaca.madre_raza or "No registrada")

    with col_padre:
        st.markdown("### Padre")
        st.write("**Nombre:**", vaca.padre_nombre or "No registrado")
        st.write("**Raza:**", vaca.padre_raza or "No registrada")

    # PRODUCCIÓN
    st.divider()
    st.subheader("Producción")

    st.metric(
        "Producción acumulada",
        f"{vaca.produccion_acumulada()} L"
    )

    st.caption(
        "En la siguiente etapa incorporaremos las gráficas "
        "y los indicadores históricos de producción."
    )
