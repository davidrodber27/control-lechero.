import streamlit as st
from datetime import date

from modelos.control_lechero import ControlLechero
from modelos.vaca import Vaca
from servicios.persistencia import (
    cargar_vacas,
    guardar_produccion
)

st.set_page_config(
    page_title="Control Lechero",
    page_icon="🐄",
    layout="wide"
)

# --------------------------------------------------
# IDENTIDAD VISUAL - CONTROL LECHERO
# --------------------------------------------------

st.markdown("""
<style>
    /* Fondo general */
    .stApp {
        background-color: #FFFFFF;
    }

    /* Barra lateral */
    [data-testid="stSidebar"] {
        background-color: #244A36;
    }

    [data-testid="stSidebar"] * {
        color: #FFFFFF;
    }

    /* Títulos */
    h1, h2, h3 {
        color: #244A36;
    }

    /* Botones principales */
    .stButton > button,
    .stFormSubmitButton > button {
        background-color: #244A36;
        color: #FFFFFF;
        border: 1px solid #244A36;
        border-radius: 10px;
        font-weight: 600;
        transition: all 0.2s ease;
    }

    /* Efecto al pasar el cursor */
    .stButton > button:hover,
    .stFormSubmitButton > button:hover {
        background-color: #78966A;
        border-color: #78966A;
        color: #FFFFFF;
    }

    /* Campos de entrada */
    [data-testid="stTextInput"] input,
    [data-testid="stNumberInput"] input,
    [data-testid="stDateInput"] input {
        border-radius: 8px;
    }

    /* Líneas divisorias */
    hr {
        border-color: #DCE5D7;
    }

    /* Mensajes y contenedores suaves */
    [data-testid="stAlert"] {
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# 1. CONFIGURACIÓN DE LA APLICACIÓN
# --------------------------------------------------



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


# --------------------------------------------------
# MENÚ LATERAL Y NAVEGACIÓN
# --------------------------------------------------

st.sidebar.title("🐄 Control Lechero")
st.sidebar.caption("Hato La Casita")
st.sidebar.divider()

st.sidebar.write(
    f"Sesión: {st.session_state.usuario.email}"
)

if st.sidebar.button("Cerrar sesión", use_container_width=True):
    supabase.auth.sign_out()
    st.session_state.usuario = None
    st.rerun()

st.sidebar.divider()

if "pagina" not in st.session_state:
    st.session_state.pagina = "Inicio"

st.sidebar.subheader("Menú principal")

if st.sidebar.button("🏠 Inicio", use_container_width=True):
    st.session_state.pagina = "Inicio"

with st.sidebar.expander("🐄 Vacas", expanded=True):
    if st.button("Registrar vaca", key="menu_registrar_vaca",
                 use_container_width=True):
        st.session_state.pagina = "Registrar vaca"

    if st.button("Vacas registradas", key="menu_vacas_registradas",
                 use_container_width=True):
        st.session_state.pagina = "Vacas registradas"

    if st.button("Administrar vacas", key="menu_administrar_vacas",
                 use_container_width=True):
        st.session_state.pagina = "Administrar vacas"

with st.sidebar.expander("🥛 Producción de leche"):
    if st.button("Registrar producción", key="menu_registrar_produccion",
                 use_container_width=True):
        st.session_state.pagina = "Registrar producción"

    if st.button("Editar producción", key="menu_editar_produccion",
                 use_container_width=True):
        st.session_state.pagina = "Editar producción"

with st.sidebar.expander("📊 Informes"):
    if st.button("Reporte diario", key="menu_reporte_diario",
                 use_container_width=True):
        st.session_state.pagina = "Reporte diario"

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





# --------------------------------------------------
# 2. DATOS TEMPORALES DE LA SESIÓN
# --------------------------------------------------





# --------------------------------------------------
# 3. ENCABEZADO
# --------------------------------------------------


# --------------------------------------------------
# PANTALLA: INICIO
# --------------------------------------------------

if st.session_state.pagina == "Inicio":

    st.title("🐄 Control Lechero")
    st.subheader("Hato La Casita")

    st.write(
        "Sistema de gestión del hato "
        "y control de producción de leche."
    )

    st.divider()

    st.header("Resumen de la finca")

    total_vacas = (
        st.session_state.finca.cantidad_vacas()
    )

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


# --------------------------------------------------
# PANTALLA: REGISTRAR VACA
# --------------------------------------------------

if st.session_state.pagina == "Registrar vaca":

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

        elif st.session_state.finca.buscar_vaca(
            identificacion_limpia
        ):
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

                # Confirmar que Supabase devolvió el registro.
                registros_guardados = respuesta.data

                if not registros_guardados:
                    st.error(
                        "No se confirmó el registro en Supabase. "
                        "Verifica la tabla antes de volver a intentarlo."
                    )

                else:
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
                            "pero no se agregó a la memoria de la aplicación. "
                            "No vuelvas a registrarla todavía."
                        )

            except Exception as error:
                st.error(
                    "No fue posible completar el registro."
                )
                st.caption(
                    "Detalle técnico del error:"
                )
                st.code(str(error))

# --------------------------------------------------
# 5.1. ADMINISTRAR VACAS
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

    vaca_edicion = st.session_state.finca.buscar_vaca(
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

        with st.form("formulario_editar_vaca"):

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
                index=razas_disponibles.index(
                    vaca_edicion.raza
                )
            )

            nueva_fecha_nacimiento = st.date_input(
                "Fecha de nacimiento",
                value=date.fromisoformat(
                    vaca_edicion.fecha_nacimiento
                ),
                min_value=date(1900, 1, 1),
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

            else:
                try:
                    datos_actualizados = {
                        "nombre": nuevo_nombre.strip(),
                        "raza": nueva_raza,
                        "fecha_nacimiento": (
                            nueva_fecha_nacimiento.isoformat()
                        )
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
                        vaca_edicion.nombre = (
                            nuevo_nombre.strip().title()
                        )
                        vaca_edicion.raza = nueva_raza
                        vaca_edicion.fecha_nacimiento = (
                            nueva_fecha_nacimiento.isoformat()
                        )

                        st.success(
                            f"Datos de {vaca_edicion.nombre} "
                            "actualizados correctamente."
                        )
                        st.rerun()

                    else:
                        st.error(
                            "Supabase no confirmó la actualización. "
                            "No se modificó la vaca en memoria."
                        )

                except Exception as error:
                    st.error(
                        "No fue posible actualizar la vaca."
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

                    del st.session_state.finca.vacas[
                        clave_vaca
                    ]

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

