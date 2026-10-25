
import streamlit as st
from supabase import create_client

from modelos.control_lechero import ControlLechero
from servicios.persistencia import cargar_vacas

from pantallas.inicio import mostrar_inicio
from pantallas.registrar_vaca import mostrar_registrar_vaca
from pantallas.vacas_registradas import mostrar_vacas_registradas
from pantallas.administrar_vacas import mostrar_administrar_vacas
from pantallas.registrar_produccion import mostrar_registrar_produccion
from pantallas.editar_produccion import mostrar_editar_produccion
from pantallas.reporte_diario import mostrar_reporte_diario


# --------------------------------------------------
# 1. CONFIGURACIÓN GENERAL
# --------------------------------------------------

st.set_page_config(
    page_title="Control Lechero",
    page_icon="🐄",
    layout="wide"
)


# --------------------------------------------------
# 2. IDENTIDAD VISUAL
# --------------------------------------------------

st.markdown(
    """
    <style>
        .stApp {
            background-color: #FFFFFF;
        }

        [data-testid="stSidebar"] {
            background-color: #244A36;
        }

        [data-testid="stSidebar"] * {
            color: #FFFFFF;
        }

        h1, h2, h3 {
            color: #244A36;
        }

        .stButton > button,
        .stFormSubmitButton > button {
            background-color: #244A36;
            color: #FFFFFF;
            border: 1px solid #244A36;
            border-radius: 10px;
            font-weight: 600;
            transition: all 0.2s ease;
        }

        .stButton > button:hover,
        .stFormSubmitButton > button:hover {
            background-color: #78966A;
            border-color: #78966A;
            color: #FFFFFF;
        }

        [data-testid="stTextInput"] input,
        [data-testid="stNumberInput"] input,
        [data-testid="stDateInput"] input {
            border-radius: 8px;
        }

        hr {
            border-color: #DCE5D7;
        }

        [data-testid="stAlert"] {
            border-radius: 10px;
        }
    </style>
    """,
    unsafe_allow_html=True
)


# --------------------------------------------------
# 3. CONEXIÓN CON SUPABASE
# --------------------------------------------------

if "supabase" not in st.session_state:
    st.session_state.supabase = create_client(
        st.secrets["SUPABASE_URL"],
        st.secrets["SUPABASE_PUBLISHABLE_KEY"]
    )

supabase = st.session_state.supabase


# --------------------------------------------------
# 4. AUTENTICACIÓN
# --------------------------------------------------

if "usuario" not in st.session_state:
    st.session_state.usuario = None


# Mostrar el formulario si no hay una sesión activa.
if st.session_state.usuario is None:

    st.title("🐄 Control Lechero")
    st.subheader("Iniciar sesión")

    with st.form("formulario_login"):

        correo = st.text_input(
            "Correo electrónico"
        )

        contrasena = st.text_input(
            "Contraseña",
            type="password"
        )

        ingresar = st.form_submit_button(
            "Ingresar"
        )

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
                st.error(
                    "No fue posible iniciar sesión."
                )

        except Exception:
            st.error(
                "No se pudo iniciar sesión. "
                "Verifica tus credenciales e inténtalo de nuevo."
            )

    st.stop()


# --------------------------------------------------
# 5. CARGAR LOS DATOS DE LA FINCA
# --------------------------------------------------

if "finca" not in st.session_state:

    try:
        finca = ControlLechero(
            "Hato La Casita"
        )

        finca = cargar_vacas(
            supabase=supabase,
            finca=finca
        )

        st.session_state.finca = finca

    except Exception as error:
        st.error(
            "No se pudieron cargar los datos de la finca."
        )
        st.code(str(error))
        st.stop()


# --------------------------------------------------
# 6. MENÚ LATERAL Y NAVEGACIÓN
# --------------------------------------------------

if "pagina" not in st.session_state:
    st.session_state.pagina = "Inicio"


st.sidebar.title("🐄 Control Lechero")
st.sidebar.caption("Hato La Casita")
st.sidebar.divider()

st.sidebar.write(
    f"Sesión: {st.session_state.usuario.email}"
)


# Cerrar sesión.
if st.sidebar.button(
    "Cerrar sesión",
    use_container_width=True
):
    try:
        supabase.auth.sign_out()
    finally:
        st.session_state.usuario = None
        st.session_state.pop("finca", None)
        st.session_state.pagina = "Inicio"
        st.rerun()


st.sidebar.divider()
st.sidebar.subheader("Menú principal")


# Pantalla de inicio.
if st.sidebar.button(
    "🏠 Inicio",
    use_container_width=True
):
    st.session_state.pagina = "Inicio"


# Menú de vacas.
with st.sidebar.expander(
    "🐄 Vacas",
    expanded=True
):

    if st.button(
        "Registrar vaca",
        key="menu_registrar_vaca",
        use_container_width=True
    ):
        st.session_state.pagina = "Registrar vaca"

    if st.button(
        "Vacas registradas",
        key="menu_vacas_registradas",
        use_container_width=True
    ):
        st.session_state.pagina = "Vacas registradas"

    if st.button(
        "Administrar vacas",
        key="menu_administrar_vacas",
        use_container_width=True
    ):
        st.session_state.pagina = "Administrar vacas"


# Menú de producción.
with st.sidebar.expander(
    "🥛 Producción de leche"
):

    if st.button(
        "Registrar producción",
        key="menu_registrar_produccion",
        use_container_width=True
    ):
        st.session_state.pagina = "Registrar producción"

    if st.button(
        "Editar producción",
        key="menu_editar_produccion",
        use_container_width=True
    ):
        st.session_state.pagina = "Editar producción"


# Menú de informes.
with st.sidebar.expander(
    "📊 Informes"
):

    if st.button(
        "Reporte diario",
        key="menu_reporte_diario",
        use_container_width=True
    ):
        st.session_state.pagina = "Reporte diario"


# --------------------------------------------------
# 7. MOSTRAR LA PANTALLA SELECCIONADA
# --------------------------------------------------

finca = st.session_state.finca
pagina = st.session_state.pagina


if pagina == "Inicio":

    mostrar_inicio(finca)


elif pagina == "Registrar vaca":

    mostrar_registrar_vaca(
        finca,
        supabase
    )


elif pagina == "Vacas registradas":

    mostrar_vacas_registradas(finca)


elif pagina == "Administrar vacas":

    mostrar_administrar_vacas(
        finca,
        supabase
    )


elif pagina == "Registrar producción":

    mostrar_registrar_produccion(
        finca,
        supabase
    )


elif pagina == "Editar producción":

    mostrar_editar_produccion(
        finca,
        supabase
    )


elif pagina == "Reporte diario":

    mostrar_reporte_diario(finca)


else:
    st.warning(
        "La pantalla seleccionada no existe. "
        "Volviendo al inicio."
    )
    st.session_state.pagina = "Inicio"
    st.rerun()
