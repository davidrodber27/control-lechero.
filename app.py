
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


import streamlit as st

if "pagina" not in st.session_state:
    st.session_state.pagina = "Inicio"

# ==========================================
# 🎨 ESTILOS CSS PERSONALIZADOS (STREAMLIT)
# ==========================================
st.markdown("""
<style>
    /* 1. Fondo de la barra lateral (Sidebar) */
    [data-testid="stSidebar"] {
        background-color: #11382B;
        color: #ffffff;
    }

    /* Ocultar elementos predeterminados molestos si es necesario */
    [data-testid="stSidebar"] hr {
        border-color: rgba(255, 255, 255, 0.15);
    }

    /* 2. Tipografías de título y subtítulo en el sidebar */
    [data-testid="stSidebar"] h1 {
        color: #ffffff;
        font-size: 1.25rem !important;
        font-weight: 700;
        padding-bottom: 0px;
    }
    [data-testid="stSidebar"] p, [data-testid="stSidebar"] span {
        color: #d1e2db;
    }

    /* 3. Estilo general para los botones del menú lateral */
    [data-testid="stSidebar"] .stButton button {
        width: 100%;
        background-color: transparent;
        color: #d1e2db;
        border: none;
        border-radius: 8px;
        text-align: left;
        padding: 10px 14px;
        font-size: 0.88rem;
        font-weight: 500;
        transition: all 0.2s ease;
        box-shadow: none;
    }

    /* Efecto Hover en los botones */
    [data-testid="stSidebar"] .stButton button:hover {
        background-color: rgba(255, 255, 255, 0.08);
        color: #ffffff;
        border: none;
    }

    /* 4. Estilo para el Botón ACTIVO (Página actual) */
    /* Usaremos una clase dinámica o el selector para resaltar la página activa */
    [data-testid="stSidebar"] .stButton button[data-baseweb="button"] {
        /* Puedes personalizar si quieres un estilo base */
    }

    /* 5. Estilo de los Expander en el sidebar */
    [data-testid="stSidebar"] [data-testid="stExpander"] {
        background-color: transparent;
        border: none;
        color: #d1e2db;
    }
    
    [data-testid="stSidebar"] details summary {
        color: #d1e2db !important;
        font-weight: 500;
        border-radius: 8px;
        padding: 8px 10px;
    }
    [data-testid="stSidebar"] details summary:hover {
        background-color: rgba(255, 255, 255, 0.08);
        color: #ffffff !important;
    }

    /* 6. Bloque de pie de página (Footer corporativo) */
    .sidebar-footer {
        margin-top: 40px;
        text-align: center;
        padding-bottom: 10px;
        border-top: 1px solid rgba(255, 255, 255, 0.12);
        padding-top: 20px;
    }
    .sidebar-footer .footer-title {
        font-size: 0.85rem;
        font-weight: 700;
        color: #ffffff;
        margin-top: 4px;
    }
    .sidebar-footer .footer-sub {
        font-size: 0.7rem;
        color: #8dae9f;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 🐄 ESTRUCTURA DE LA BARRA LATERAL
# ==========================================

with st.sidebar:
    # 1. Cabecera / Logo principal
    st.markdown("### 🐄 Control Lechero")
    st.caption("Hato La Casita")
    st.divider()

    # 2. Menú principal (Ítems directos y expansores ordenados)
    
    # Inicio
    if st.button("🏠 Inicio", use_container_width=True, key="btn_inicio"):
        st.session_state.pagina = "Inicio"
        st.rerun()

    # Menú de vacas (Reemplazando o ajustando el expander para que luzca plano como en el diseño)
    # Nota: Si prefieres lista directa sin expander tal como muestra la primera imagen, puedes listarlos así:
    st.markdown("<p style='font-size: 0.75rem; color: #8dae9f; margin: 12px 0 4px 10px; text-transform: uppercase; letter-spacing: 0.5px;'>Gestión de Vacas</p>", unsafe_allow_html=True)
    
    if st.button("➕ Registrar vaca", use_container_width=True, key="menu_registrar_vaca"):
        st.session_state.pagina = "Registrar vaca"
        st.rerun()

    if st.button("📋 Vacas registradas", use_container_width=True, key="menu_vacas_registradas"):
        st.session_state.pagina = "Vacas registradas"
        st.rerun()

    if st.button("⚙️ Administrar vacas", use_container_width=True, key="menu_administrar_vacas"):
        st.session_state.pagina = "Administrar vacas"
        st.rerun()

    st.divider()

    # Menú de producción
    st.markdown("<p style='font-size: 0.75rem; color: #8dae9f; margin: 12px 0 4px 10px; text-transform: uppercase; letter-spacing: 0.5px;'>Producción</p>", unsafe_allow_html=True)
    
    if st.button("🥛 Registrar producción", use_container_width=True, key="menu_registrar_produccion"):
        st.session_state.pagina = "Registrar producción"
        st.rerun()

    if st.button("✏️ Editar producción", use_container_width=True, key="menu_editar_produccion"):
        st.session_state.pagina = "Editar producción"
        st.rerun()

    st.divider()

    # Menú de informes
    st.markdown("<p style='font-size: 0.75rem; color: #8dae9f; margin: 12px 0 4px 10px; text-transform: uppercase; letter-spacing: 0.5px;'>Informes</p>", unsafe_allow_html=True)
    
    if st.button("📊 Reporte diario", use_container_width=True, key="menu_reporte_diario"):
        st.session_state.pagina = "Reporte diario"
        st.rerun()

    st.divider()

    # 3. Sección de Sesión y Usuario (movida al final del menú de navegación, como en la referencia)
    st.markdown(f"👤 <span style='font-size: 0.8rem;'>Sesión: {st.session_state.usuario.email if hasattr(st.session_state, 'usuario') and st.session_state.usuario else 'Invitado'}</span>", unsafe_allow_html=True)
    
    if st.button("🚪 Cerrar sesión", use_container_width=True, key="btn_cerrar_sesion"):
        try:
            supabase.auth.sign_out()
        except Exception:
            pass
        finally:
            st.session_state.usuario = None
            st.session_state.pop("finca", None)
            st.session_state.pagina = "Inicio"
            st.rerun()

    # 4. Footer / Branding inferior de la barra lateral ("Tradición que produce futuro")
    st.markdown("""
        <div class="sidebar-footer">
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
