
import streamlit as st
from datetime import date
from modelos.vaca import Vaca

def mostrar_administrar_vacas(finca, supabase):

    st.divider()
    st.header("Administrar vacas")

    accion_vaca = st.radio(
        "¿Qué deseas hacer?",
        ["Editar vaca", "Eliminar vaca"],
        horizontal=True,
        key="accion_vaca"
    )

    vacas_edicion = finca.vacas

    if not vacas_edicion:
        st.info("No hay vacas registradas para administrar.")

    else:
        opciones_edicion = {
            f"{vaca.identificacion} - {vaca.nombre}":
            vaca.identificacion
            for vaca in vacas_edicion.values()
        }

        vaca_seleccionada_edicion = st.selectbox(
            "Selecciona la vaca",
            options=list(opciones_edicion.keys()),
            key="vaca_seleccionada_edicion"
        )

        identificacion_edicion = opciones_edicion[
            vaca_seleccionada_edicion
        ]

        vaca_edicion = finca.buscar_vaca(
            identificacion_edicion
        )

        if vaca_edicion is None:
            st.error("No se encontró la vaca seleccionada.")

       
        elif accion_vaca == "Editar vaca":

            razas_disponibles = [
                "Holstein",
                "Jersey",
                "Normando",
                "Cruce",
                "Otra"
            ]

            if vaca_edicion.raza not in razas_disponibles:
                razas_disponibles.append(vaca_edicion.raza)

            # Recuperar los datos reproductivos actuales
            numero_partos_actual = vaca_edicion.numero_partos

            fecha_parto_actual = (
                date.fromisoformat(vaca_edicion.fecha_ultimo_parto)
                if vaca_edicion.fecha_ultimo_parto
                else None
            )

            with st.form("formulario_editar_vaca"):

                st.subheader("Datos generales")

                st.text_input(
                    "Identificación (no editable por ahora)",
                    value=vaca_edicion.identificacion,
                    disabled=True
                )

                nuevo_nombre = st.text_input(
                    "Nombre",
                    value=vaca_edicion.nombre
                )

                nueva_raza = st.selectbox(
                    "Raza",
                    options=razas_disponibles,
                    index=razas_disponibles.index(vaca_edicion.raza)
                )

                nueva_fecha_nacimiento = st.date_input(
                    "Fecha de nacimiento",
                    value=date.fromisoformat(
                        vaca_edicion.fecha_nacimiento
                    ),
                    min_value=date(1900, 1, 1),
                    max_value=date.today()
                )

                st.divider()
                st.subheader("Datos reproductivos")

                nuevo_numero_partos = st.number_input(
                    "Número de partos registrados",
                    min_value=0,
                    value=numero_partos_actual,
                    step=1
                )

                nueva_fecha_ultimo_parto = st.date_input(
                    "Fecha del último parto",
                    value=fecha_parto_actual,
                    min_value=date.fromisoformat(
                        vaca_edicion.fecha_nacimiento
                    ),
                    max_value=date.today()
                )

                guardar_cambios = st.form_submit_button(
                    "Guardar cambios"
                )

            if guardar_cambios:

                if not nuevo_nombre.strip():
                    st.error(
                        "El nombre de la vaca no puede estar vacío."
                    )

                elif nuevo_numero_partos > 0 and nueva_fecha_ultimo_parto is None:
                    st.error(
                        "Debes seleccionar la fecha del último parto."
                    )

                elif nuevo_numero_partos == 0 and nueva_fecha_ultimo_parto is not None:
                    st.error(
                        "Si la vaca no ha tenido partos, "
                        "la fecha del último parto debe quedar vacía."
                    )

                else:
                    try:
                        # Validar los datos mediante el modelo Vaca
                        vaca_validada = Vaca(
                            nombre=nuevo_nombre.strip(),
                            fecha_nacimiento=nueva_fecha_nacimiento,
                            raza=nueva_raza,
                            identificacion=vaca_edicion.identificacion,
                            fecha_ultimo_parto=nueva_fecha_ultimo_parto,
                            numero_partos=int(nuevo_numero_partos)
                        )

                        datos_actualizados = {
                            "nombre": vaca_validada.nombre,
                            "raza": vaca_validada.raza,
                            "fecha_nacimiento": (
                                vaca_validada.fecha_nacimiento
                            ),
                            "fecha_ultimo_parto": (
                                vaca_validada.fecha_ultimo_parto
                            ),
                            "numero_partos": vaca_validada.numero_partos
                        }

                        respuesta = (
                            supabase
                            .table("vacas")
                            .update(datos_actualizados)
                            .eq(
                                "identificacion",
                                identificacion_edicion
                            )
                            .execute()
                        )

                        if respuesta.data:

                            # Actualizar también el objeto en memoria
                            vaca_edicion.nombre = vaca_validada.nombre
                            vaca_edicion.raza = vaca_validada.raza
                            vaca_edicion.fecha_nacimiento = (
                                vaca_validada.fecha_nacimiento
                            )
                            vaca_edicion.fecha_ultimo_parto = (
                                vaca_validada.fecha_ultimo_parto
                            )
                            vaca_edicion.numero_partos = (
                                vaca_validada.numero_partos
                            )

                            st.success(
                                f"Datos de {vaca_edicion.nombre} "
                                "actualizados correctamente."
                            )

                            st.rerun()

                        else:
                            st.error(
                                "Supabase no confirmó la actualización."
                            )

                    except Exception as error:
                        st.error(
                            "No fue posible actualizar los datos de la vaca."
                        )
                        st.code(str(error))


        elif accion_vaca == "Eliminar vaca":

            st.warning(
                f"Vas a eliminar a {vaca_edicion.nombre} "
                f"(identificación: "
                f"{vaca_edicion.identificacion})."
            )

            st.error(
                "Atención: al eliminar esta vaca, también se puede "
                "eliminar todo su historial de producción."
            )

            confirmar_eliminacion = st.checkbox(
                "Confirmo que deseo eliminar esta vaca y su "
                "posible historial de producción.",
                key="confirmar_eliminacion_vaca"
            )

            if st.button(
                "Eliminar vaca definitivamente",
                disabled=not confirmar_eliminacion,
                key="boton_eliminar_vaca"
            ):
                try:
                    respuesta = (
                        supabase
                        .table("vacas")
                        .delete()
                        .eq(
                            "identificacion",
                            identificacion_edicion
                        )
                        .execute()
                    )

                    if respuesta.data:
                        clave_vaca = (
                            identificacion_edicion.strip().upper()
                        )

                        del finca.vacas[clave_vaca]

                        st.success(
                            f"La vaca {vaca_edicion.nombre} "
                            "fue eliminada correctamente."
                        )
                        st.rerun()

                    else:
                        st.error(
                            "Supabase no confirmó la eliminación. "
                            "La vaca se conserva en memoria."
                        )

                except Exception as error:
                    st.error(
                        "No fue posible eliminar la vaca."
                    )
                    st.code(str(error))

