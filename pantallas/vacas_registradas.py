
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
                st.write("**Nombre:**", vaca.nombre)

                st.write(
                    "**Identificación:**",
                    vaca.identificacion
                )

                st.write("**Raza:**", vaca.raza)

                st.write(
                    "**Fecha de nacimiento:**",
                    date.fromisoformat(
                        vaca.fecha_nacimiento
                    ).strftime("%d/%m/%Y")
                )

                st.write(
                    "**Edad actual:**",
                    vaca.edad_actual
                )

                st.write(
                    "**Producción acumulada:**",
                    f"{vaca.produccion_acumulada()} L"
                )

    else:
        st.info(
            "Todavía no hay vacas registradas. "
            "Utiliza el formulario para agregar la primera."
        )
