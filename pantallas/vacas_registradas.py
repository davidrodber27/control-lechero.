
import streamlit as st
from datetime import date


def mostrar_vacas_registradas(finca):

    st.divider()
    st.header("Vacas registradas")

    vacas_registradas = finca.vacas

    if vacas_registradas:

        for vaca in vacas_registradas.values():

            with st.expander(
                f"{vaca.identificacion} - {vaca.nombre}"
            ):

                # Datos generales
                st.subheader("Datos generales")

                st.write("**Nombre:**", vaca.nombre)
                st.write("**Identificación:**", vaca.identificacion)
                st.write("**Raza:**", vaca.raza)

                st.write(
                    "**Fecha de nacimiento:**",
                    date.fromisoformat(
                        vaca.fecha_nacimiento
                    ).strftime("%d/%m/%Y")
                )

                st.write("**Edad actual:**", vaca.edad_actual)

                # Datos reproductivos
                st.divider()
                st.subheader("Control reproductivo")

                st.write(
                    "**Número de partos:**",
                    vaca.numero_partos
                )

                if vaca.fecha_ultimo_parto is not None:

                    fecha_parto = date.fromisoformat(
                        vaca.fecha_ultimo_parto
                    )

                    st.write(
                        "**Último parto:**",
                        fecha_parto.strftime("%d/%m/%Y")
                    )

                    st.metric(
                        "Días posparto",
                        vaca.dias_posparto
                    )

                else:
                    st.info("No hay fecha de parto registrada.")

                st.write("**Estado de preñez:** Pendiente de diagnóstico")
                st.caption(
                    "El estado de preñez se actualizará cuando "
                    "incorporemos el registro de servicios y diagnósticos."
                )

                # Producción
                st.divider()
                st.subheader("Producción")

                st.write(
                    "**Producción acumulada:**",
                    f"{vaca.produccion_acumulada()} L"
                )

    else:
        st.info(
            "Todavía no hay vacas registradas. "
            "Utiliza el formulario para agregar la primera."
        )

