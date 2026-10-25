
import streamlit as st
from datetime import date


def mostrar_editar_produccion(finca, supabase):

    st.divider()
    st.header("Editar producción registrada")

    vacas_con_registros = [
        vaca
        for vaca in finca.vacas.values()
        if vaca.registros
    ]

    if not vacas_con_registros:

        st.info(
            "Todavía no hay registros de producción para editar."
        )

    else:

        opciones_edicion = {
            f"{vaca.identificacion} - {vaca.nombre}":
            vaca.identificacion
            for vaca in vacas_con_registros
        }

        with st.form("formulario_edicion_produccion"):

            vaca_edicion = st.selectbox(
                "Selecciona la vaca",
                options=list(opciones_edicion.keys())
            )

            identificacion_edicion = opciones_edicion[
                vaca_edicion
            ]

            vaca_objetivo = finca.buscar_vaca(
                identificacion_edicion
            )

            fechas_disponibles = sorted(
                vaca_objetivo.registros.keys(),
                reverse=True
            )

            fecha_edicion_texto = st.selectbox(
                "Selecciona la fecha del registro",
                options=fechas_disponibles,
                format_func=lambda fecha: (
                    date.fromisoformat(fecha).strftime("%d/%m/%Y")
                )
            )

            registro_actual = vaca_objetivo.registros[
                fecha_edicion_texto
            ]

            st.caption(
                "Valores guardados actualmente. "
                "Al guardar, se reemplazarán por los nuevos."
            )

            col1, col2 = st.columns(2)

            with col1:
                nuevos_litros_manana = st.number_input(
                    "Litros de la mañana",
                    min_value=0,
                    step=1,
                    value=registro_actual["litros_manana"],
                    key="editar_litros_manana"
                )

            with col2:
                nuevos_litros_tarde = st.number_input(
                    "Litros de la tarde",
                    min_value=0,
                    step=1,
                    value=registro_actual["litros_tarde"],
                    key="editar_litros_tarde"
                )

            nuevo_potrero = st.selectbox(
                "Potrero",
                options=list(range(1, 13)),
                index=registro_actual["potrero"] - 1,
                key="editar_potrero"
            )

            confirmar_edicion = st.form_submit_button(
                "Guardar cambios"
            )

        if confirmar_edicion:

            try:
                # 1. Actualizar primero el registro en Supabase.
                respuesta = (
                    supabase
                    .table("produccion")
                    .update({
                        "litros_manana": int(nuevos_litros_manana),
                        "litros_tarde": int(nuevos_litros_tarde),
                        "potrero": int(nuevo_potrero)
                    })
                    .eq(
                        "identificacion",
                        identificacion_edicion
                    )
                    .eq(
                        "fecha",
                        fecha_edicion_texto
                    )
                    .execute()
                )

                if respuesta.data:

                    # 2. Actualizar la memoria solo si Supabase
                    # devuelve el registro actualizado.
                    actualizado = finca.actualizar_produccion(
                        identificacion=identificacion_edicion,
                        fecha=fecha_edicion_texto,
                        litros_manana=int(nuevos_litros_manana),
                        litros_tarde=int(nuevos_litros_tarde),
                        potrero=int(nuevo_potrero)
                    )

                    if actualizado:
                        st.success(
                            "Producción actualizada en Supabase "
                            "y en la aplicación."
                        )
                        st.rerun()
                    else:
                        st.warning(
                            "Supabase actualizó el registro, pero "
                            "no se pudo actualizar la memoria. "
                            "Recarga la aplicación para sincronizar."
                        )

                else:
                    st.error(
                        "Supabase no devolvió el registro actualizado. "
                        "Verifica el registro antes de volver a intentarlo."
                    )

            except Exception as error:
                st.error(
                    "No fue posible actualizar la producción."
                )
                st.caption("Detalle técnico del error:")
                st.code(str(error))
