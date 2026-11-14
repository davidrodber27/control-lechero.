
import streamlit as st
from datetime import date

from servicios.persistencia import guardar_produccion


def mostrar_registrar_produccion(finca, supabase):

    st.divider()
    st.header("Registrar producción de leche")
    # Mostrar el mensaje de confirmación después de guardar.
    if "mensaje_produccion" in st.session_state:
        st.success(st.session_state.mensaje_produccion)
        del st.session_state.mensaje_produccion

    vacas_disponibles = finca.vacas

    if not vacas_disponibles:
        st.info("Primero debes registrar al menos una vaca.")
        return

    opciones_vacas = {
        f"{vaca.identificacion} - {vaca.nombre}": vaca.identificacion
        for vaca in vacas_disponibles.values()
    }

    st.write(
        "Registra individualmente la producción de cada vaca "
        "en el ordeño que ya se realizó."
    )

    with st.form("formulario_produccion"):

        vaca_seleccionada = st.selectbox(
            "Selecciona la vaca",
            options=list(opciones_vacas.keys())
        )

        fecha_produccion = st.date_input(
            "Fecha de producción",
            value=date.today(),
            max_value=date.today()
        )

        orden = st.selectbox(
            "Selecciona el ordeño",
            options=["Mañana", "Tarde"]
        )

        litros = st.number_input(
            f"Litros del ordeño de la {orden.lower()}",
            min_value=0,
            step=1,
            value=0
        )

        potrero = st.selectbox(
            "Potrero donde estuvo la vaca",
            options=list(range(1, 13))
        )

        enviar_produccion = st.form_submit_button(
            "Guardar ordeño",
            use_container_width=True
        )

    if enviar_produccion:

        identificacion = opciones_vacas[vaca_seleccionada]

        try:
            respuesta = guardar_produccion(
                supabase=supabase,
                identificacion=identificacion,
                fecha=fecha_produccion,
                orden=(
                    "manana"
                    if orden == "Mañana"
                    else "tarde"
                ),
                litros=int(litros),
                potrero=int(potrero)
            )

            if respuesta is not None:

                st.session_state.mensaje_produccion = (
                    f"¡Almacenado con éxito! Se registraron "
                    f"{int(litros)} litros del ordeño de la "
                    f"{orden.lower()} para {vaca_seleccionada}."
                )
            
                st.rerun()
        except Exception as error:
            st.error(
                "No se pudo guardar el ordeño. "
                "Verifica los datos e inténtalo nuevamente."
            )
            st.code(str(error))

