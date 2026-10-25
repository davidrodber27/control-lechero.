
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




# ==============================================================================
# 1. CONFIGURACIÓN INICIAL DEL ESTADO
# ==============================================================================
if "pagina" not in st.session_state:
    st.session_state.pagina = "Inicio"

# ==============================================================================
# 2. ESTILOS CSS PERSONALIZADOS (Aumento de letra, colores y diseño modular)
# ==============================================================================
st.markdown("""
<style>
    /* Fondo general de la barra lateral (Sidebar) */
    [data-testid="stSidebar"] {
        background-color: #11382B;
        color: #ffffff;
        padding-top: 1rem;
    }

    /* Aumento de tamaño de letra general en el menú */
    [data-testid="stSidebar"] .stButton button {
        width: 100%;
        background-color: transparent;
        color: #d1e2db;
        border: none;
        border-radius: 8px;
        text-align: left;
        padding: 12px 14px; /* Mayor espacio y presencia */
        font-size: 1.2rem;  /* Letra aumentada */
        font-weight: 500;
        transition: all 0.2s ease;
        box-shadow: none;
    }

    /* Efecto Hover para los botones del menú */
    [data-testid="stSidebar"] .stButton button:hover {
        background-color: rgba(255, 255, 255, 0.08);
        color: #ffffff;
        border: none;
    }

    /* Estilo especial para el botón activo (Inicio u otros seleccionados) */
    /* Puedes aplicar una clase o identificar el botón activo */
    [data-testid="stSidebar"] .stButton button[kind="secondary"] {
        /* Estilos base */
    }

    /* Líneas divisorias sutiles */
    [data-testid="stSidebar"] hr {
        border-color: rgba(255, 255, 255, 0.15);
        margin: 14px 0;
    }

    /* Estilo para la sección de sesión en BLANCO */
    .sidebar-session-text {
        color: #ffffff !important;
        font-size: 1rem;
        font-weight: 500;
        padding: 4px 0;
    }

    /* Estilo del Footer inferior */
    .sidebar-footer {
        margin-top: 30px;
        text-align: center;
        padding-top: 15px;
        border-top: 1px solid rgba(255, 255, 255, 0.12);
    }
    .footer-title {
        font-size: 2rem;
        font-weight: 700;
        color: #ffffff;
        margin-top: 60px;
    }
    .footer-sub {
        font-size: 0.75rem;
        color: #8dae9f;
    }
</style>
""", unsafe_allow_html=True)


# ==============================================================================
# 3. CONSTRUCCIÓN DE LA BARRA LATERAL (MENÚ MODULAR)
# ==============================================================================
with st.sidebar:

    # --------------------------------------------------------------------------
    # BLOQUE A: CABECERA / LOGO SUPERIOR
    # (Editable de forma única)
    # --------------------------------------------------------------------------
    with st.container():
        st.markdown("<h2 style='text-align: center; color: white; font-size: 1.3rem; margin-bottom: 0;'>🐄 Control Lechero</h2>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #a3c2b5; font-size: 0.8rem; margin-top: 2px;'>Hato La Casita</p>", unsafe_allow_html=True)
    
    st.divider()

    # --------------------------------------------------------------------------
    # BLOQUE B: NAVEGACIÓN PRINCIPAL (INICIO Y VACAS)
    # (Editable de forma única)
    # --------------------------------------------------------------------------
    with st.container():
        # Botón Inicio (Puedes resaltar este si st.session_state.pagina == "Inicio")
        if st.button("🏠  Inicio", use_container_width=True, key="menu_inicio"):
            st.session_state.pagina = "Inicio"
            st.rerun()

        if st.button("🐮  Registrar vaca", use_container_width=True, key="menu_registrar_vaca"):
            st.session_state.pagina = "Registrar vaca"
            st.rerun()

        if st.button("📋  Vacas registradas", use_container_width=True, key="menu_vacas_registradas"):
            st.session_state.pagina = "Vacas registradas"
            st.rerun()

        if st.button("⚙️  Administrar vacas", use_container_width=True, key="menu_administrar_vacas"):
            st.session_state.pagina = "Administrar vacas"
            st.rerun()

    st.divider()

    # --------------------------------------------------------------------------
    # BLOQUE C: MÓDULO DE PRODUCCIÓN
    # (Editable de forma única)
    # --------------------------------------------------------------------------
    with st.container():
        if st.button("🥛  Registrar producción", use_container_width=True, key="menu_registrar_produccion"):
            st.session_state.pagina = "Registrar producción"
            st.rerun()

        if st.button("✏️  Editar producción", use_container_width=True, key="menu_editar_produccion"):
            st.session_state.pagina = "Editar producción"
            st.rerun()

    st.divider()

    # --------------------------------------------------------------------------
    # BLOQUE D: MÓDULO DE INFORMES Y REPORTES
    # (Editable de forma única)
    # --------------------------------------------------------------------------
    with st.container():
        if st.button("📊  Reporte diario", use_container_width=True, key="menu_reporte_diario"):
            st.session_state.pagina = "Reporte diario"
            st.rerun()

    st.divider()

    # --------------------------------------------------------------------------
    # BLOQUE E: SESIÓN Y USUARIO (TEXTO EN BLANCO)
    # (Editable de forma única)
    # --------------------------------------------------------------------------
    with st.container():
        usuario_email = st.session_state.usuario.email if hasattr(st.session_state, 'usuario') and st.session_state.usuario else "usuario@finca.com"
        
        # Texto de sesión en blanco puro
        st.markdown(f"""
            <div style="display: flex; align-items: center; gap: 10px; padding: 6px 14px;">
                <span style="font-size: 1.1rem;">👤</span>
                <span class="sidebar-session-text">Sesión: {usuario_email}</span>
            </div>
        """, unsafe_allow_html=True)

        if st.button("🚪  Cerrar sesión", use_container_width=True, key="menu_cerrar_sesion"):
            try:
                supabase.auth.sign_out()
            except Exception:
                pass
            finally:
                st.session_state.usuario = None
                st.session_state.pop("finca", None)
                st.session_state.pagina = "Inicio"
                st.rerun()

    # --------------------------------------------------------------------------
    # BLOQUE F: PIE DE PÁGINA / FOOTER CORPORATIVO
    # (Editable de forma única)
    # --------------------------------------------------------------------------
    st.markdown("""
        <div class="sidebar-footer">
            <div style="font-size: 1.2rem; margin-bottom: 2px;">⛰️</div>
            <div class="footer-title">Hato La Casita</div>
            <div class="footer-sub">Tradición que produce futuro</div>
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
