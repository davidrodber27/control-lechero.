import streamlit as st
from datetime import date

from modelos.control_lechero import ControlLechero
from modelos.vaca import Vaca
from servicios.persistencia import (
    cargar_vacas,
    guardar_produccion
)

# --------------------------------------------------
# 1. CONFIGURACIÓN DE LA APLICACIÓN
# --------------------------------------------------

st.set_page_config(
    page_title="Control Lechero",
    page_icon="🐄",
    layout="wide"
)

from supabase import create_client

# Crear un cliente independiente por sesión de Streamlit.
if "supabase" not in st.session_state:
    st.session_state.supabase = create_client(
        st.secrets["SUPABASE_URL"],
        st.secrets["SUPABASE_PUBLISHABLE_KEY"]
    )

supabase = st.session_state.supabase

# Inicializar el estado de autenticación.
if "usuario" not in st.session_state:
    st.session_state.usuario = None

# Mostrar el inicio de sesión si no hay usuario autenticado.
if st.session_state.usuario is None:
    st.title("Control Lechero")
    st.subheader("Iniciar sesión")

    with st.form("formulario_login"):
        correo = st.text_input("Correo electrónico")
        contrasena = st.text_input(
            "Contraseña",
            type="password"
        )
        ingresar = st.form_submit_button("Ingresar")

    if ingresar:
        try:
            respuesta = supabase.auth.sign_in_with_password({
                "email": correo.strip(),
                "password": contrasena
            })

            if respuesta.user is not None:
                st.session_state.usuario = respuesta.user
                st.rerun()
            else:
                st.error("No fue posible iniciar sesión.")

        except Exception:
            st.error(
                "No se pudo iniciar sesión. "
                "Verifica tus credenciales e inténtalo de nuevo."
            )

    st.stop()

# Mostrar el usuario autenticado y permitir cerrar sesión.
st.sidebar.write(
    f"Sesión: {st.session_state.usuario.email}"
)

# --------------------------------------------------
# CARGAR LA FINCA DESDE SUPABASE
# --------------------------------------------------

if "finca" not in st.session_state:
    try:
        finca = ControlLechero("Hato La Casita")

        finca = cargar_vacas(
            supabase=supabase,
            finca=finca
        )

        st.session_state.finca = finca

    except Exception as error:
        st.error("No se pudieron cargar los datos de la finca.")
        st.code(str(error))
        st.stop()


try:
    respuesta_produccion = (
        supabase.table("produccion")
        .select("*")
        .execute()
    )

    st.success("Conexión con la tabla produccion correcta.")
    st.write(
        "Registros encontrados:",
        len(respuesta_produccion.data)
    )

except Exception as error:
    st.error("No se pudo consultar la tabla produccion.")
    st.write(str(error))

if st.sidebar.button("Cerrar sesión"):
    supabase.auth.sign_out()
    st.session_state.usuario = None
    st.rerun()


# --------------------------------------------------
# 2. DATOS TEMPORALES DE LA SESIÓN
# --------------------------------------------------


if "finca" not in st.session_state:
    finca = ControlLechero("Hato La Casita")

    try:
        finca = cargar_vacas(
            supabase=supabase,
            finca=finca
        )

        st.session_state.finca = finca

    except Exception:
        st.error(
            "No se pudieron cargar los datos de la finca "
            "desde la base de datos."
        )
        st.stop()


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
                    nombre=nombre.strip(),
                    fecha_nacimiento=fecha_nacimiento,
                    raza=raza,
                    identificacion=identificacion.strip()
                )

                # Verificar que la vaca no exista en memoria.
                existente = (
                    st.session_state.finca.buscar_vaca(
                        identificacion.strip()
                    )
                )

                if existente:
                    st.error(
                        "Ya existe una vaca con esa identificación."
                    )

                else:
                    # Guardar la vaca en Supabase.
                    datos_vaca = {
                        "identificacion": identificacion.strip(),
                        "nombre": nombre.strip(),
                        "raza": raza,
                        "fecha_nacimiento": (
                            fecha_nacimiento.isoformat()
                        )
                    }

                    respuesta = (
                        supabase.table("vacas")
                        .insert(datos_vaca)
                        .execute()
                    )

                    # Agregarla a la memoria de la aplicación.
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
                        st.warning(
                            "La vaca se guardó en Supabase, "
                            "pero no se agregó a la memoria "
                            "de la aplicación. "
                            "No vuelvas a registrarla todavía."
                        )

            except Exception as error:
                st.error(
                    "No fue posible completar el registro."
                )
                st.write(str(error))

# --------------------------------------------------
# 5.1. EDITAR DATOS DE UNA VACA
# --------------------------------------------------

st.divider()
st.header("Administrar vacas")

accion_vaca = st.radio(
    "¿Qué deseas hacer?",
    ["Editar vaca", "Eliminar vaca"],
    horizontal=True,
    key="accion_vaca"
)

vacas_edicion = st.session_state.finca.vacas

if not vacas_edicion:
    st.info("No hay vacas registradas para editar.")

else:
    opciones_edicion = {
        f"{vaca.identificacion} - {vaca.nombre}":
        vaca.identificacion
        for vaca in vacas_edicion.values()
    }

    vaca_seleccionada_edicion = st.selectbox(
        "Selecciona la vaca que deseas editar",
        options=list(opciones_edicion.keys()),
        key="vaca_seleccionada_edicion"
    )

    identificacion_edicion = opciones_edicion[
        vaca_seleccionada_edicion
    ]

    vaca_edicion = st.session_state.finca.buscar_vaca(
        identificacion_edicion
    )

    with st.form("formulario_editar_vaca"):

        st.text_input(
            "Identificación (no editable)",
            value=vaca_edicion.identificacion,
            disabled=True
        )

        nuevo_nombre = st.text_input(
            "Nombre",
            value=vaca_edicion.nombre
        )

        nueva_raza = st.selectbox(
            "Raza",
            [
                "Holstein",
                "Jersey",
                "Normando",
                "Cruce",
                "Otra"
            ],
            index=[
                "Holstein",
                "Jersey",
                "Normando",
                "Cruce",
                "Otra"
            ].index(vaca_edicion.raza)
            if vaca_edicion.raza in [
                "Holstein",
                "Jersey",
                "Normando",
                "Cruce",
                "Otra"
            ] else 4
        )

        nueva_fecha_nacimiento = st.date_input(
            "Fecha de nacimiento",
            value=date.fromisoformat(
                vaca_edicion.fecha_nacimiento
            ),
            max_value=date.today()
        )

        guardar_cambios = st.form_submit_button(
            "Guardar cambios"
        )

        if guardar_cambios:
            st.info(
                "Formulario preparado. En el siguiente paso "
                "conectaremos estos cambios con Supabase."
            )

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
                # 1. Buscar la vaca en la finca.
                vaca = st.session_state.finca.buscar_vaca(
                    identificacion
                )

                if vaca is None:
                    st.error("No se encontró la vaca seleccionada.")

                # 2. Comprobar si ya existe producción para esa fecha.
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

                    # 4. Actualizar la finca en memoria
                    # solo si Supabase devuelve el registro.
                    if respuesta:
                        registrado = (
                            st.session_state.finca.registrar_produccion(
                                identificacion=identificacion,
                                fecha=fecha_produccion,
                                litros_manana=int(litros_manana),
                                litros_tarde=int(litros_tarde),
                                potrero=int(potrero)
                            )
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


# --------------------------------------------------
# 8. REPORTE DIARIO DE PRODUCCIÓN
# --------------------------------------------------

st.divider()
st.header("Reporte diario de producción")

fecha_reporte = st.date_input(
    "Selecciona la fecha que deseas consultar",
    value=date.today(),
    max_value=date.today(),
    key="fecha_reporte"
)

finca = st.session_state.finca

produccion_total = finca.produccion_total(fecha_reporte)

col1, col2 = st.columns(2)

with col1:
    st.metric(
        "Producción total del día",
        f"{produccion_total} L"
    )

with col2:
    registros_dia = sum(
        1
        for vaca in finca.vacas.values()
        if fecha_reporte.isoformat() in vaca.registros
    )

    st.metric(
        "Vacas con producción registrada",
        registros_dia
    )

# Construir el detalle por vaca
datos_vacas = []

for vaca in finca.vacas.values():

    registro = vaca.registros.get(
        fecha_reporte.isoformat()
    )

    if registro is not None:

        total_vaca = (
            registro["litros_manana"]
            + registro["litros_tarde"]
        )

        datos_vacas.append({
            "Identificación": vaca.identificacion,
            "Vaca": vaca.nombre,
            "Mañana (L)": registro["litros_manana"],
            "Tarde (L)": registro["litros_tarde"],
            "Total (L)": total_vaca,
            "Potrero": registro["potrero"]
        })

st.subheader("Producción por vaca")

if datos_vacas:
    st.dataframe(
        datos_vacas,
        use_container_width=True,
        hide_index=True
    )
else:
    st.info(
        "No hay producción registrada para esta fecha."
    )

# Producción agrupada por potrero
st.subheader("Producción por potrero")

produccion_potreros = finca.produccion_por_potrero(
    fecha_reporte
)

if produccion_potreros:

    datos_potreros = [
        {
            "Potrero": potrero,
            "Producción (L)": litros
        }
        for potrero, litros in sorted(
            produccion_potreros.items()
        )
    ]

    st.dataframe(
        datos_potreros,
        use_container_width=True,
        hide_index=True
    )

else:
    st.info(
        "No hay producción asociada a potreros "
        "para esta fecha."
    )


# --------------------------------------------------
# 9. EDITAR PRODUCCIÓN REGISTRADA
# --------------------------------------------------

st.divider()
st.header("Editar producción registrada")

finca = st.session_state.finca
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
                actualizado = finca.actualizar_produccion(
                    identificacion=identificacion_edicion,
                    fecha=fecha_edicion_texto,
                    litros_manana=int(nuevos_litros_manana),
                    litros_tarde=int(nuevos_litros_tarde),
                    potrero=nuevo_potrero
                )

                if actualizado:
                    st.success(
                        "Producción actualizada correctamente."
                    )
                    st.rerun()
                else:
                    st.warning(
                        "No se encontró un registro para actualizar."
                    )

            except (ValueError, TypeError) as error:
                st.error(str(error))

