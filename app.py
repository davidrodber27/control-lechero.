import streamlit as st
from datetime import date
from pantallas.editar_produccion import mostrar_editar_produccion
from pantallas.registrar_produccion import mostrar_registrar_produccion
from pantallas.administrar_vacas import mostrar_administrar_vacas
from pantallas.vacas_registradas import mostrar_vacas_registradas
from pantallas.inicio import mostrar_inicio
from pantallas.registrar_vaca import mostrar_registrar_vaca
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
    mostrar_inicio(st.session_state.finca)


# --------------------------------------------------
# 4. RESUMEN DE LA FINCA
# --------------------------------------------------




# --------------------------------------------------
# 5. FORMULARIO PARA REGISTRAR VACAS
# --------------------------------------------------


# --------------------------------------------------
# PANTALLA: REGISTRAR VACA
# --------------------------------------------------

if st.session_state.pagina == "Registrar vaca":
    mostrar_registrar_vaca(
        st.session_state.finca,
        supabase
    )

# --------------------------------------------------
# 5.1. ADMINISTRAR VACAS
# --------------------------------------------------
if st.session_state.pagina == "Administrar vacas":
    mostrar_administrar_vacas(
        st.session_state.finca,
        supabase
    )

# --------------------------------------------------
# 6. LISTADO DE VACAS
# --------------------------------------------------
if st.session_state.pagina == "Vacas registradas":
    mostrar_vacas_registradas(
        st.session_state.finca
    )


# --------------------------------------------------
# 7. REGISTRAR PRODUCCIÓN DE LECHE
# --------------------------------------------------


if st.session_state.pagina == "Registrar producción":
    mostrar_registrar_produccion(
        st.session_state.finca,
        supabase
    )

# --------------------------------------------------
# 8. REPORTE DIARIO DE PRODUCCIÓN
# --------------------------------------------------
if st.session_state.pagina == "Reporte diario":
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
if st.session_state.pagina == "Editar producción":
    mostrar_editar_produccion(
        st.session_state.finca,
        supabase
    )
