
import streamlit as st
from datetime import date

from modelos.control_lechero import ControlLechero
from modelos.vaca import Vaca
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

produccion_hoy = (
    st.session_state.finca.produccion_total(date.today())
)

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Vacas registradas", total_vacas)

with col2:
    st.metric(
        "Producción de hoy",
        f"{produccion_hoy} L"
    )

with col3:
    st.metric("Potreros", 12)


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

vacas_registradas = st.session_state.finca.vacas

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


# --------------------------------------------------
# 7. REGISTRAR PRODUCCIÓN DE LECHE
# --------------------------------------------------

st.divider()
st.header("Registrar producción de leche")

vacas_disponibles = st.session_state.finca.vacas

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
                registrado = (
                    st.session_state.finca.registrar_produccion(
                        identificacion=identificacion,
                        fecha=fecha_produccion,
                        litros_manana=int(litros_manana),
                        litros_tarde=int(litros_tarde),
                        potrero=potrero
                    )
                )

                if registrado:
                    total_dia = (
                        int(litros_manana)
                        + int(litros_tarde)
                    )

                    st.success(
                        f"Producción registrada: {total_dia} L "
                        f"para {vaca_seleccionada}."
                    )
                else:
                    st.warning(
                        "Esta vaca ya tiene un registro para esa fecha. "
                        "No se modificaron los datos existentes."
                    )

            except (ValueError, TypeError) as error:
                st.error(str(error))

