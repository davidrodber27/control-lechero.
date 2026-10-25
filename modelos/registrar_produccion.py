
import streamlit as st
from datetime import date

from servicios.persistencia import guardar_produccion


def mostrar_registrar_produccion(finca, supabase):

    st.divider()
    st.header("Registrar producción de leche")

    vacas_disponibles = finca.vacas

    if not vacas_disponibles:

        st.info("Primero debes registrar al menos una vaca.")

    else:

        opciones_vacas = {
            f"{vaca.identificacion} - {vaca.nombre}":
            vaca.identificacion
            for vaca in vacas_disponibles.values()
        }

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

            col1, col2 = st.columns(2)

            with col1:
                litros_manana = st.number_input(
                    "Litros del ordeño de la mañana",
                    min_value=0,
                    step=1,
                    value=0
                )

            with col2:
                litros_tarde = st.number_input(
                    "Litros del ordeño de la tarde",
                    min_value=0,
                    step=1,
                    value=0
                )

            potrero = st.selectbox(
                "Potrero donde estuvo la vaca",
                options=list(range(1, 13))
            )

            enviar_produccion = st.form_submit_button(
                "Guardar producción"
            )

        if enviar_produccion:

            identificacion = opciones_vacas[
                vaca_seleccionada
            ]

            try:
                # 1. Buscar la vaca en la finca.
                vaca = finca.buscar_vaca(identificacion)

                if vaca is None:
                    st.error("No se encontró la vaca seleccionada.")

                # 2. Evitar duplicados para la misma fecha.
                elif fecha_produccion.isoformat() in vaca.registros:
                    st.warning(
                        "Esta vaca ya tiene un registro para esa fecha. "
                        "No se modificaron los datos existentes."
                    )

                else:
                    # 3. Guardar primero en Supabase.
                    respuesta = guardar_produccion(
                        supabase=supabase,
                        identificacion=identificacion,
                        fecha=fecha_produccion,
                        litros_manana=int(litros_manana),
                        litros_tarde=int(litros_tarde),
                        potrero=int(potrero)
                    )

                    # 4. Actualizar la memoria solo si hay respuesta.
                    if respuesta:
                        registrado = finca.registrar_produccion(
                            identificacion=identificacion,
                            fecha=fecha_produccion,
                            litros_manana=int(litros_manana),
                            litros_tarde=int(litros_tarde),
                            potrero=int(potrero)
                        )

                        if registrado:
                            total_dia = (
                                int(litros_manana)
                                + int(litros_tarde)
                            )

                            st.success(
                                f"Producción guardada en Supabase: "
                                f"{total_dia} L para "
                                f"{vaca_seleccionada}."
                            )
                        else:
                            st.warning(
                                "El registro se guardó en Supabase, "
                                "pero no se pudo actualizar la finca "
                                "en memoria. Recarga la aplicación."
                            )
                    else:
                        st.error(
                            "Supabase no confirmó el registro. "
                            "No se actualizó la finca en memoria."
                        )

            except Exception as error:
                st.error(
                    "No se pudo guardar la producción. "
                    "Verifica los datos e inténtalo de nuevo."
                )
                st.code(str(error))
