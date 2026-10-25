import html
import streamlit as st
import base64
from supabase import create_client
from pathlib import Path
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
# ESTILO PROFESIONAL DEL MENÚ LATERAL
# ============================================================
st.markdown("""
<style>
    [data-testid="stSidebar"] {
        background: #102F25;
    }

    [data-testid="stSidebar"] > div:first-child {
        padding-top: 1.2rem;
    }

    /* Encabezado de la finca */
    
    .sidebar-brand {
        text-align: center;
        padding: 8px 4px 16px;
    }
    
    .sidebar-logo {
        display: block;
        width: 100px;
        height: 100px;
        object-fit: contain;
        margin: 0 auto 12px;
    }
    
    .brand-name {
        color: #FFFFFF;
        font-size: 1.55rem;
        font-weight: 800;
        letter-spacing: -0.5px;
        line-height: 1.2;
        margin: 0;
        text-align: center;
    }
    
    .brand-subtitle {
        color: #B5CBBF;
        font-size: 0.95rem;
        font-weight: 500;
        margin-top: 8px;
        text-align: center;
    }


    .menu-label {
        color: #91B09F;
        font-size: 0.70rem;
        font-weight: 700;
        letter-spacing: 1.3px;
        text-transform: uppercase;
        margin: 12px 0 7px 4px;
    }

    /* Botones uniformes */
    [data-testid="stSidebar"] .stButton > button {
        width: 100%;
        min-height: 45px;
        justify-content: flex-start;
        border-radius: 9px;
        padding: 9px 12px;
        font-size: 0.92rem;
        font-weight: 500;
        text-align: left;
        transition: all 0.18s ease;
        box-shadow: none;
    }

    /* Opciones no seleccionadas */
    [data-testid="stSidebar"] .stButton > button[kind="secondary"] {
        background: transparent;
        color: #D6E4DC;
        border: 1px solid transparent;
    }

    [data-testid="stSidebar"] .stButton > button[kind="secondary"]:hover {
        background: #214637;
        color: #FFFFFF;
        border-color: #315744;
    }

    /* Pantalla activa */
    [data-testid="stSidebar"] .stButton > button[kind="primary"] {
        background: #DCEADF;
        color: #173D2D;
        border: 1px solid #DCEADF;
        font-weight: 700;
    }

    [data-testid="stSidebar"] .stButton > button[kind="primary"]:hover {
        background: #ECF4ED;
        color: #173D2D;
    }

    [data-testid="stSidebar"] .stButton button p {
        font-size: 0.92rem;
    }

    [data-testid="stSidebar"] hr {
        border: none;
        border-top: 1px solid rgba(255,255,255,0.13);
        margin: 15px 0;
    }

    .sidebar-user {
        color: #FFFFFF;
        font-size: 0.83rem;
        line-height: 1.5;
        overflow-wrap: anywhere;
    }

    .sidebar-user-label {
        color: #9DBBAA;
        font-size: 0.72rem;
        margin-bottom: 3px;
    }

    .sidebar-footer {
        text-align: center;
        padding: 17px 5px 5px;
        margin-top: 18px;
        border-top: 1px solid rgba(255,255,255,0.13);
    }

    .footer-title {
        color: #E8F0EA;
        font-size: 0.9rem;
        font-weight: 700;
    }

    .footer-sub {
        color: #91B09F;
        font-size: 0.72rem;
        margin-top: 4px;
    }
</style>
""", unsafe_allow_html=True)



# ============================================================
# MENÚ LATERAL
# ============================================================
with st.sidebar:

    # Marca: logo y encabezado
    
    ruta_logo = (
        Path(__file__).resolve().parent.parent
        / "assets"
        / "logo_vaca.png"
    )
    carpeta_proyecto = Path(__file__).resolve().parent
    carpeta_assets = carpeta_proyecto / "assets"

    st.sidebar.write("Carpeta del proyecto:", str(carpeta_proyecto))
    st.sidebar.write("Contenido de la carpeta:", [
        elemento.name
        for elemento in carpeta_proyecto.iterdir()
    ])

    if carpeta_assets.exists():
        st.sidebar.write("Contenido de assets:", [
            elemento.name
            for elemento in carpeta_assets.iterdir()
        ])
    else:
        st.sidebar.error("No existe la carpeta assets.")


    if ruta_logo.is_file():
        logo_base64 = base64.b64encode(
            ruta_logo.read_bytes()
        ).decode("utf-8")

        st.markdown(
            f"""
            <div class="sidebar-brand">
                <img
                    class="sidebar-logo"
                    src="data:image/png;base64,{logo_base64}"
                    alt="Logo de Hato La Casita"
                />
                <div class="brand-name">Control Lechero</div>
                <div class="brand-subtitle">Hato La Casita</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            """
            <div class="sidebar-brand">
                <div class="brand-name">Control Lechero</div>
                <div class="brand-subtitle">Hato La Casita</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.divider()

    # Navegación principal
    st.markdown(
        '<div class="menu-label">General</div>',
        unsafe_allow_html=True,
    )

    opciones_principales = [
        ("Inicio", "Inicio", ":material/home:"),
        ("Registrar vaca", "Registrar vaca", ":material/pets:"),
        ("Vacas registradas", "Vacas registradas", ":material/list_alt:"),
        ("Administrar vacas", "Administrar vacas", ":material/settings:"),
    ]

    for texto, pagina, icono in opciones_principales:
        if st.button(
            texto,
            key=f"menu_{pagina.lower().replace(' ', '_')}",
            icon=icono,
            use_container_width=True,
            type=(
                "primary"
                if st.session_state.pagina == pagina
                else "secondary"
            ),
        ):
            st.session_state.pagina = pagina
            st.rerun()

    # Menú de producción
    st.markdown(
        '<div class="menu-label">Producción</div>',
        unsafe_allow_html=True,
    )

    opciones_produccion = [
        (
            "Registrar producción",
            "Registrar producción",
            ":material/water_drop:",
        ),
        (
            "Editar producción",
            "Editar producción",
            ":material/edit:",
        ),
        (
            "Reporte diario",
            "Reporte diario",
            ":material/analytics:",
        ),
    ]

    for texto, pagina, icono in opciones_produccion:
        if st.button(
            texto,
            key=f"menu_{pagina.lower().replace(' ', '_')}",
            icon=icono,
            use_container_width=True,
            type=(
                "primary"
                if st.session_state.pagina == pagina
                else "secondary"
            ),
        ):
            st.session_state.pagina = pagina
            st.rerun()

    st.divider()

    # Información del usuario
    usuario = st.session_state.get("usuario")

    usuario_email = (
        getattr(usuario, "email", None)
        if usuario is not None
        else None
    )

    usuario_email = usuario_email or "Usuario no identificado"
    correo_seguro = html.escape(str(usuario_email))

    st.markdown(
        f"""
        <div style="padding: 7px 4px 12px;">
            <div class="sidebar-user-label">SESIÓN ACTUAL</div>
            <div class="sidebar-user">{correo_seguro}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Cerrar sesión
    if st.button(
        "Cerrar sesión",
        key="menu_cerrar_sesion",
        icon=":material/logout:",
        use_container_width=True,
        type="secondary",
    ):
        try:
            supabase.auth.sign_out()
        except Exception:
            pass

        st.session_state.usuario = None
        st.session_state.pop("finca", None)
        st.session_state.pagina = "Inicio"
        st.rerun()

    # Pie de página
    st.markdown(
        """
        <div class="sidebar-footer">
            <div class="footer-title">Hato La Casita</div>
            <div class="footer-sub">Tradición que produce futuro</div>
        </div>
        """,
        unsafe_allow_html=True,
    )



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
