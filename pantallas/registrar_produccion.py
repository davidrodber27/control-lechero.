
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

                # Buscar el objeto de la vaca en memoria.
                vaca = finca.buscar_vaca(identificacion)

                if vaca is None:
                    raise ValueError(
                        "El ordeño se guardó en Supabase, "
                        "pero no se encontró la vaca en memoria."
                    )

                # Comprobar si ya existe un registro para esa fecha.
                fecha_clave = fecha_produccion.isoformat()

                registro_actual = vaca.registros.get(fecha_clave)

                # Conservar el ordeño que ya estuviera registrado.
                if registro_actual is None:
                    litros_manana = None
                    litros_tarde = None
                else:
                    litros_manana = registro_actual["litros_manana"]
                    litros_tarde = registro_actual["litros_tarde"]

                # Actualizar únicamente el ordeño seleccionado.
                if orden == "Mañana":
                    litros_manana = int(litros)
                else:
                    litros_tarde = int(litros)

                # Crear o actualizar el registro en el objeto Vaca.
                if registro_actual is None:
                    vaca.registrar_produccion(
                        fecha=fecha_produccion,
                        litros_manana=litros_manana,
                        litros_tarde=litros_tarde,
                        potrero=int(potrero)
                    )
                else:
                    vaca.actualizar_produccion(
                        fecha=fecha_produccion,
                        litros_manana=litros_manana,
                        litros_tarde=litros_tarde,
                        potrero=int(potrero)
                    )

                st.session_state.mensaje_produccion = (
                    f"¡Almacenado con éxito! Se registraron "
                    f"{int(litros)} litros del ordeño de la "
                    f"{orden.lower()} para {vaca_seleccionada}."
                )

                st.rerun()

            else:
                st.error(
                    "Supabase no confirmó el registro del ordeño."
                )

        except Exception as error:
            st.error(
                "No se pudo completar el proceso de registro."
            )
            st.code(str(error))

