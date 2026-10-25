
import streamlit as st
from datetime import date

from modelos.vaca import Vaca


def mostrar_registrar_vaca(finca, supabase):

    st.title("Registrar una vaca")
    st.write(
        "Registra la identificación y los datos "
        "generales de cada animal."
    )

    with st.form("formulario_vaca"):

        identificacion = st.text_input(
            "Identificación de la vaca",
            placeholder="Ejemplo: V001"
        )

        nombre = st.text_input(
            "Nombre de la vaca",
            placeholder="Ejemplo: Roja"
        )

        raza = st.selectbox(
            "Raza",
            [
                "Holstein",
                "Jersey",
                "Normando",
                "Cruce",
                "Otra"
            ]
        )

        fecha_nacimiento = st.date_input(
            "Fecha de nacimiento",
            value=date.today(),
            max_value=date.today()
        )

        enviar = st.form_submit_button("Registrar vaca")

    if enviar:

        identificacion_limpia = identificacion.strip()
        nombre_limpio = nombre.strip()

        if not identificacion_limpia:
            st.error(
                "Debes escribir la identificación de la vaca."
            )

        elif not nombre_limpio:
            st.error(
                "Debes escribir el nombre de la vaca."
            )

        elif finca.buscar_vaca(identificacion_limpia):
            st.error(
                "Ya existe una vaca con esa identificación."
            )

        else:
            try:
                nueva_vaca = Vaca(
                    nombre=nombre_limpio,
                    fecha_nacimiento=fecha_nacimiento,
                    raza=raza,
                    identificacion=identificacion_limpia
                )

                datos_vaca = {
                    "identificacion": identificacion_limpia,
                    "nombre": nombre_limpio,
                    "raza": raza,
                    "fecha_nacimiento": fecha_nacimiento.isoformat()
                }

                respuesta = (
                    supabase.table("vacas")
                    .insert(datos_vaca)
                    .execute()
                )

                registros_guardados = respuesta.data

                if not registros_guardados:
                    st.error(
                        "No se confirmó el registro en Supabase. "
                        "Verifica la tabla antes de volver a intentarlo."
                    )

                else:
                    agregada = finca.agregar_vaca(nueva_vaca)

                    if agregada:
                        st.success(
                            f"Vaca {nueva_vaca.nombre} "
                            "registrada correctamente."
                        )
                    else:
                        st.warning(
                            "La vaca se guardó en Supabase, "
                            "pero no se agregó a la memoria de la aplicación. "
                            "No vuelvas a registrarla todavía."
                        )

            except Exception as error:
                st.error(
                    "No fue posible completar el registro."
                )
                st.caption("Detalle técnico del error:")
                st.code(str(error))

