from modelos.vaca import Vaca
import streamlit as st
from datetime import date

from modelos.control_lechero import ControlLechero

# --------------------------------------------------
# 1. CONFIGURACIÓN DE LA APLICACIÓN
# --------------------------------------------------

st.set_page_config(
    page_title="Control Lechero",
    page_icon="🐄",
    layout="wide"
)

# --------------------------------------------------
# 2. DATOS TEMPORALES DE LA SESIÓN
# --------------------------------------------------

if "finca" not in st.session_state:
    st.session_state.finca = ControlLechero(
        "Hato La Casita"
    )

# --------------------------------------------------
# 3. ENCABEZADO
# --------------------------------------------------

st.title("🐄 Control Lechero")
st.subheader("Hato La Casita")

st.write(
    "Sistema de gestión del hato "
    "y control de producción de leche."
)

st.divider()

# --------------------------------------------------
# 4. RESUMEN DE LA FINCA
# --------------------------------------------------

st.header("Resumen de la finca")

total_vacas = st.session_state.finca.cantidad_vacas()

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Vacas registradas", total_vacas)

with col2:
    st.metric("Producción de hoy", "0 L")

with col3:
    st.metric("Potreros", 12)

st.divider()

# --------------------------------------------------
# 5. FORMULARIO PARA REGISTRAR VACAS
# --------------------------------------------------

st.header("Registrar una vaca")

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

    enviar = st.form_submit_button(
        "Registrar vaca"
    )

    
    if enviar:

        if not identificacion.strip():
            st.error(
                "Debes escribir la identificación de la vaca."
            )

        elif not nombre.strip():
            st.error(
                "Debes escribir el nombre de la vaca."
            )

        else:
            try:
                nueva_vaca = Vaca(
                    nombre=nombre,
                    fecha_nacimiento=fecha_nacimiento,
                    raza=raza,
                    identificacion=identificacion
                )

                agregada = (
                    st.session_state.finca.agregar_vaca(
                        nueva_vaca
                    )
                )

                if agregada:
                    st.success(
                        f"Vaca {nueva_vaca.nombre} "
                        "registrada correctamente."
                    )
                else:
                    st.error(
                        "Ya existe una vaca con esa identificación."
                    )

            except (ValueError, TypeError) as error:
                st.error(str(error))


# --------------------------------------------------
# 6. LISTADO DE VACAS
# --------------------------------------------------

st.divider()
st.header("Vacas registradas")

if st.session_state.finca.vacas:

    for vaca in st.session_state.vacas:

        with st.expander(
            f'{vaca["identificacion"]} - {vaca["nombre"]}'
        ):
            st.write("**Nombre:**", vaca["nombre"])
            st.write(
                "**Identificación:**",
                vaca["identificacion"]
            )
            st.write("**Raza:**", vaca["raza"])
            st.write(
                "**Fecha de nacimiento:**",
                vaca["fecha_nacimiento"].strftime("%d/%m/%Y")
            )

else:
    st.info(
        "Todavía no hay vacas registradas. "
        "Utiliza el formulario para agregar la primera."
    )

st.caption(
    "Versión de aprendizaje: los registros actuales "
    "se conservan solo durante la sesión."
)

