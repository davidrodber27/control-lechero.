import html
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


# ============================================================
# 6. ESTADO INICIAL
# ============================================================
if "pagina" not in st.session_state:
    st.session_state.pagina = "Inicio"


# ============================================================
# 6.1. ESTILOS DEL MENÚ LATERAL
# ============================================================
st.markdown("""
<style>
    /* Fondo de la barra lateral */
    [data-testid="stSidebar"] {
        background-color: #11382B;
    }

    [data-testid="stSidebar"] > div:first-child {
        padding-top: 1rem;
    }

    /* Botones del menú */
    [data-testid="stSidebar"] .stButton > button {
        width: 100%;
        min-height: 44px;
        background-color: transparent;
        color: #E3EEE8;
        border: 1px solid transparent;
        border-radius: 8px;
        text-align: left;
        padding: 10px 14px;
        font-size: 1rem;
        font-weight: 500;
        box-shadow: none;
        transition: background-color 0.2s ease;
    }

    /* Efecto al pasar el cursor */
    [data-testid="stSidebar"] .stButton > button:hover {
        background-color: rgba(255, 255, 255, 0.10);
        color: #FFFFFF;
        border-color: rgba(255, 255, 255, 0.12);
    }

    /* Separadores */
    [data-testid="stSidebar"] hr {
        border-color: rgba(255, 255, 255, 0.16);
        margin: 14px 0;
    }

    /* Información de sesión */
    .sidebar-session-text {
        color: #FFFFFF !important;
        font-size: 0.85rem;
        font-weight: 500;
        overflow-wrap: anywhere;
    }

    /* Pie de página */
    .sidebar-footer {
        margin-top: 24px;
        padding: 18px 8px 8px;
        text-align: center;
        border-top: 1px solid rgba(255, 255, 255, 0.16);
    }

    .footer-title {
        font-size: 1.25rem;
        font-weight: 700;
        color: #FFFFFF;
        margin-top: 6px;
    }

    .footer-sub {
        font-size: 0.75rem;
        color: #A3C2B5;
        margin-top: 5px;
    }

    /* Ajustes para pantallas pequeñas */
    @media (max-width: 700px) {
        [data-testid="stSidebar"] .stButton > button {
            font-size: 0.95rem;
            padding: 9px 10px;
        }
    }
</style>
""", unsafe_allow_html=True)


# ============================================================
# 6.2. CONSTRUCCIÓN DEL MENÚ LATERAL
# ============================================================
with st.sidebar:

    # --------------------------------------------------------
    # A. ENCABEZADO
    # --------------------------------------------------------
    st.markdown("""
        <div style="text-align:center; padding: 8px 0 12px;">
            <div style="font-size:1.5rem; font-weight:700; color:#FFFFFF;">
                🐄 Control Lechero
            </div>
            <div style="font-size:0.85rem; color:#A3C2B5; margin-top:5px;">
                Hato La Casita
            </div>
        </div>
    """, unsafe_allow_html=True)

    st.divider()

    # --------------------------------------------------------
    # B. NAVEGACIÓN PRINCIPAL
    # --------------------------------------------------------
    if st.button("🏠  Inicio", key="menu_inicio",
                 use_container_width=True):
        st.session_state.pagina = "Inicio"
        st.rerun()

    if st.button("🐮  Registrar vaca", key="menu_registrar_vaca",
                 use_container_width=True):
        st.session_state.pagina = "Registrar vaca"
        st.rerun()

    if st.button("📋  Vacas registradas", key="menu_vacas_registradas",
                 use_container_width=True):
        st.session_state.pagina = "Vacas registradas"
        st.rerun()

    if st.button("⚙️  Administrar vacas", key="menu_administrar_vacas",
                 use_container_width=True):
        st.session_state.pagina = "Administrar vacas"
        st.rerun()

    st.divider()

    # --------------------------------------------------------
    # C. PRODUCCIÓN
    # --------------------------------------------------------
    if st.button("🥛  Registrar producción",
                 key="menu_registrar_produccion",
                 use_container_width=True):
        st.session_state.pagina = "Registrar producción"
        st.rerun()

    if st.button("✏️  Editar producción",
                 key="menu_editar_produccion",
                 use_container_width=True):
        st.session_state.pagina = "Editar producción"
        st.rerun()

    st.divider()

    # --------------------------------------------------------
    # D. INFORMES
    # --------------------------------------------------------
    if st.button("📊  Reporte diario", key="menu_reporte_diario",
                 use_container_width=True):
        st.session_state.pagina = "Reporte diario"
        st.rerun()

    st.divider()

    # --------------------------------------------------------
    # E. USUARIO Y CIERRE DE SESIÓN
    # --------------------------------------------------------
    usuario = st.session_state.get("usuario")
    usuario_email = (
        getattr(usuario, "email", None)
        if usuario is not None
        else None
    )

    if not usuario_email:
        usuario_email = "Usuario no identificado"

    correo_seguro = html.escape(str(usuario_email))

    st.markdown(
        f"""
        <div style="display:flex; align-items:flex-start; gap:10px;
                    padding:8px 4px;">
            <span style="font-size:1.1rem;">👤</span>
            <span class="sidebar-session-text">
                Sesión:<br>{correo_seguro}
            </span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if st.button("🚪  Cerrar sesión", key="menu_cerrar_sesion",
                 use_container_width=True):
        try:
            supabase.auth.sign_out()
        except Exception:
            pass

        st.session_state.usuario = None
        st.session_state.pop("finca", None)
        st.session_state.pagina = "Inicio"
        st.rerun()

    # --------------------------------------------------------
    # F. PIE DE PÁGINA
    # --------------------------------------------------------
    st.markdown("""
        <div class="sidebar-footer">
            <div style="font-size:1.5rem;">⛰️</div>
            <div class="footer-title">Hato La Casita</div>
            <div class="footer-sub">
                Tradición que produce futuro
            </div>
        </div>
    """, unsafe_allow_html=True)

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
