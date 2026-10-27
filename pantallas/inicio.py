
import base64
import mimetypes
from datetime import date
from pathlib import Path

import streamlit as st


# ============================================================
# 1. RUTAS Y UTILIDADES
# ============================================================

RUTA_PROYECTO = Path(__file__).resolve().parent.parent
RUTA_ASSETS = RUTA_PROYECTO / "assets"


def imagen_base64(nombre_archivo):
    """Devuelve el tipo MIME y la imagen codificada, si existe."""
    ruta = RUTA_ASSETS / nombre_archivo

    if not ruta.is_file():
        return None, None

    tipo_imagen, _ = mimetypes.guess_type(str(ruta))

    if not tipo_imagen or not tipo_imagen.startswith("image/"):
        return None, None

    contenido = base64.b64encode(ruta.read_bytes()).decode("utf-8")
    return tipo_imagen, contenido


def crear_logo_html(
    nombre_archivo,
    clase_css,
    texto_alternativo,
    emoji_fallback="🌱",
):
    """Construye el HTML de un logo o muestra un emoji alternativo."""
    tipo_imagen, contenido = imagen_base64(nombre_archivo)

    if not contenido:
        return f'<span class="hato-logo-fallback">{emoji_fallback}</span>'

    return (
        f'<img src="data:{tipo_imagen};base64,{contenido}" '
        f'alt="{texto_alternativo}" '
        f'class="{clase_css}" />'
    )


# ============================================================
# 2. ESTILOS
# ============================================================

def cargar_estilos(foto_cabecera, paisaje):
    """Carga los estilos visuales del panel principal."""

    if foto_cabecera:
        tipo_foto, contenido_foto = foto_cabecera
        fondo_cabecera = (
            f'url("data:{tipo_foto};base64,{contenido_foto}")'
        )
    else:
        fondo_cabecera = (
            "linear-gradient(120deg, #244A36, #557B5E)"
        )

    if paisaje:
        tipo_paisaje, contenido_paisaje = paisaje
        fondo_tarjetas = (
            f'url("data:{tipo_paisaje};base64,{contenido_paisaje}")'
        )
    else:
        fondo_tarjetas = (
            "linear-gradient(145deg, #F7FCF8, #EAF4ED)"
        )

    st.markdown(
        f"""
        <style>
            /* ---------- Cabecera ---------- */

            .hato-hero {{
                min-height: 360px;
                padding: 42px;
                margin-bottom: 28px;
                border-radius: 18px;
                overflow: hidden;
                box-sizing: border-box;
                display: flex;
                align-items: center;
                background-image:
                    linear-gradient(
                        90deg,
                        rgba(12, 43, 29, 0.70),
                        rgba(12, 43, 29, 0.30),
                        rgba(12, 43, 29, 0.05)
                    ),
                    {fondo_cabecera};
                background-size: cover;
                background-position: center 58%;
                box-shadow: 0 8px 24px rgba(22, 52, 35, 0.14);
            }}

            .hato-hero-content {{
                max-width: 580px;
            }}

            .hato-hero-eyebrow {{
                color: #E0EBDD !important;
                font-size: 12px;
                font-weight: 700;
                letter-spacing: 2px;
                margin-bottom: 10px;
            }}

            .hato-hero-title {{
                color: #FFFFFF !important;
                font-size: 38px !important;
                font-weight: 800 !important;
                line-height: 1.15 !important;
                margin: 0 0 12px 0 !important;
                padding: 0 !important;
                background: transparent !important;
                border: none !important;
            }}

            .hato-hero-description {{
                color: #FFFFFF !important;
                font-size: 15px !important;
                line-height: 1.6 !important;
                max-width: 380px;
                margin: 0 !important;
            }}

            /* ---------- Títulos ---------- */

            .hato-section-title {{
                color: #244A36;
                font-size: 22px;
                font-weight: 750;
                margin: 8px 0 4px 0;
            }}

            .hato-section-subtitle {{
                color: #69786D;
                font-size: 14px;
                margin: 0 0 18px 0;
            }}

            /* ---------- Indicadores ---------- */

            .hato-kpi {{
                border-radius: 20px;
                padding: 26px 16px 22px;
                min-height: 300px;
                text-align: center;
                box-sizing: border-box;
                box-shadow: 0 5px 18px rgba(36, 90, 58, 0.07);
            }}

            .hato-kpi-vacas,
            .hato-kpi-cesped {{
                background: linear-gradient(145deg, #F7FCF8, #EDF7F0);
                border: 1px solid #D9EADF;
            }}

            .hato-kpi-produccion {{
                background: linear-gradient(145deg, #F7FBFF, #EAF3FC);
                border: 1px solid #D5E5F5;
            }}

            .hato-kpi-icon-circle {{
                width: 76px;
                height: 76px;
                margin: 0 auto 20px;
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
                box-shadow: 0 6px 14px rgba(34, 105, 65, 0.18);
            }}

            .hato-kpi-vacas .hato-kpi-icon-circle,
            .hato-kpi-cesped .hato-kpi-icon-circle {{
                background: linear-gradient(145deg, #78B88B, #287849 55%, #174D32);
            }}

            .hato-kpi-produccion .hato-kpi-icon-circle {{
                background: linear-gradient(145deg, #78B4E8, #2878BE 55%, #164A7A);
            }}

            .hato-kpi-logo {{
                width: 43px;
                height: 43px;
                object-fit: contain;
                filter: brightness(0) invert(1);
            }}

            .hato-logo-fallback {{
                font-size: 36px;
                line-height: 1;
            }}

            .hato-kpi-label {{
                color: #28583C;
                font-size: 1.05rem;
                font-weight: 700;
                line-height: 1.4;
                margin-bottom: 10px;
            }}

            .hato-kpi-produccion .hato-kpi-label {{
                color: #245581;
            }}

            .hato-kpi-value {{
                color: #174D32;
                font-size: 2.6rem;
                font-weight: 800;
                line-height: 1.15;
                margin: 4px 0 12px;
                overflow-wrap: anywhere;
            }}

            .hato-kpi-produccion .hato-kpi-value {{
                color: #164A7A;
            }}

            .hato-kpi-divider {{
                width: 54px;
                height: 2px;
                border-radius: 2px;
                background: #A6CDB1;
                margin: 0 auto 10px;
            }}

            .hato-kpi-produccion .hato-kpi-divider {{
                background: #A7CBEA;
            }}

            .hato-kpi-unit {{
                color: #63836D;
                font-size: 0.72rem;
                font-weight: 700;
                letter-spacing: 2px;
                line-height: 1.4;
            }}

            .hato-kpi-produccion .hato-kpi-unit {{
                color: #6485A5;
            }}

            /* ---------- Tarjetas de accesos rápidos ---------- */

            .st-key-inicio-card-produccion,
            .st-key-inicio-card-vaca,
            .st-key-inicio-card-reporte {{
                background-image:
                    linear-gradient(
                        145deg,
                        rgba(247, 252, 248, 0.91),
                        rgba(234, 244, 237, 0.89)
                    ),
                    {fondo_tarjetas};
                background-size: cover;
                background-position: center;
                border: 1px solid #D9EADF;
                border-radius: 20px;
                padding: 24px 20px 20px;
                min-height: 300px;
                box-sizing: border-box;
                box-shadow: 0 5px 18px rgba(36, 90, 58, 0.09);
            }}

            .hato-action-content {{
                text-align: center;
                min-height: 210px;
            }}

            
            .hato-action-icon-circle {{
                width: 76px;
                height: 76px;
                margin: 0 auto 20px;
                border-radius: 50%;
                background: transparent;
                display: flex;
                align-items: center;
                justify-content: center;
                overflow: visible;
                box-shadow: none;
            }}

            .hato-action-logo {{
                width: 52px;
                height: 52px;
                object-fit: contain;
                display: block;
                background: transparent;
                border: none;
                box-shadow: none;
            }}

            /* Vaca: imagen circular, sin círculo verde exterior */
            .hato-action-icon-circle:has(.hato-action-logo-cow) {{
                width: 76px;
                height: 76px;
                overflow: hidden;
                border-radius: 50%;
                background: transparent;
                box-shadow: none;
            }}

            .hato-action-logo-cow {{
                width: 76px;
                height: 76px;
                object-fit: cover;
                object-position: center;
                border-radius: 50%;
                display: block;
                background: transparent;
            }}

            .hato-action-logo-cow img {{
                width: 100%;
                height: 100%;
                object-fit: cover;
                object-position: center;
                border-radius: 50%;
                display: block;
            }}

            /* Barras: sin círculo ni fondo */
            .hato-action-icon-circle:has(.hato-action-logo-bars) {{
                background: transparent;
                box-shadow: none;
                border: none;
                overflow: visible;
            }}

            .hato-action-logo-bars {{
                width: 58px;
                height: 58px;
                object-fit: contain;
                background: transparent;
                border: none;
                box-shadow: none;

                /* Convierte el icono blanco en verde */
                filter: brightness(0) saturate(100%)
                        invert(35%) sepia(70%) saturate(600%)
                        hue-rotate(90deg) brightness(90%);
            }}

            .hato-action-title {{
                color: #244A36;
                font-size: 1.08rem;
                font-weight: 750;
                line-height: 1.4;
                margin-bottom: 10px;
            }}

            .hato-action-description {{
                color: #52685A;
                font-size: 0.88rem;
                line-height: 1.55;
                min-height: 44px;
                margin-bottom: 12px;
            }}

            .st-key-inicio-card-produccion div.stButton > button,
            .st-key-inicio-card-vaca div.stButton > button,
            .st-key-inicio-card-reporte div.stButton > button {{
                width: 100%;
                min-height: 42px;
                border-radius: 10px;
                font-weight: 650;
                border: 1px solid #C8DDCE;
                background: #FFFFFF;
                color: #24583A;
            }}

            .st-key-inicio-card-produccion div.stButton > button:hover,
            .st-key-inicio-card-vaca div.stButton > button:hover,
            .st-key-inicio-card-reporte div.stButton > button:hover {{
                background: #E4F2E8;
                border-color: #8EB99A;
                color: #174D32;
            }}

            /* ---------- Adaptación a móviles ---------- */

            @media (max-width: 700px) {{
                .hato-hero {{
                    min-height: 230px;
                    padding: 24px 20px;
                }}

                .hato-hero-title {{
                    font-size: 30px !important;
                }}

                .hato-hero-description {{
                    font-size: 14px !important;
                }}

                .hato-kpi {{
                    min-height: 260px;
                    padding: 22px 10px;
                }}

                .hato-kpi-value {{
                    font-size: 2rem;
                }}

                .st-key-inicio-card-produccion,
                .st-key-inicio-card-vaca,
                .st-key-inicio-card-reporte {{
                    padding: 20px 12px;
                    min-height: 290px;
                }}
            }}
        </style>

        <div class="hato-hero">
            <div class="hato-hero-content">
                <div class="hato-hero-eyebrow">
                    HATO LA CASITA · GESTIÓN GANADERA
                </div>
                <h1 class="hato-hero-title">Hato La Casita</h1>
                <p class="hato-hero-description">
                    Bienvenido al centro de control de tu finca.
                    Consulta la producción y administra tu hato
                    desde un solo lugar.
                </p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# 3. TARJETAS DE INDICADORES
# ============================================================

def mostrar_indicador(
    columna,
    clase_tarjeta,
    nombre_logo,
    clase_logo,
    texto_alternativo,
    titulo,
    valor,
    unidad,
    emoji,
):
    """Muestra una tarjeta de indicador con su logo."""

    logo = crear_logo_html(
        nombre_logo,
        f"hato-kpi-logo {clase_logo}",
        texto_alternativo,
        emoji,
    )

    tarjeta_html = f"""
    <div class="hato-kpi {clase_tarjeta}">
        <div class="hato-kpi-icon-circle">
            {logo}
        </div>
        <div class="hato-kpi-label">{titulo}</div>
        <div class="hato-kpi-value">{valor}</div>
        <div class="hato-kpi-divider"></div>
        <div class="hato-kpi-unit">{unidad}</div>
    </div>
    """

    with columna:
        st.markdown(tarjeta_html, unsafe_allow_html=True)


# ============================================================
# 4. ACCESOS RÁPIDOS
# ============================================================

def mostrar_acceso(
    columna,
    clave_contenedor,
    nombre_logo,
    clase_logo,
    texto_alternativo,
    emoji,
    titulo,
    descripcion,
    texto_boton,
    clave_boton,
    destino,
):
    """Muestra una tarjeta de acceso y gestiona su navegación."""

    with columna:
        with st.container(key=clave_contenedor):
            logo = crear_logo_html(
                nombre_logo,
                f"hato-action-logo {clase_logo}",
                texto_alternativo,
                emoji,
            )

            st.markdown(
                f"""
                <div class="hato-action-content">
                    <div class="hato-action-icon-circle">
                        {logo}
                    </div>
                    <div class="hato-action-title">{titulo}</div>
                    <div class="hato-action-description">
                        {descripcion}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            if st.button(
                texto_boton,
                key=clave_boton,
                use_container_width=True,
            ):
                st.session_state.pagina = destino
                st.rerun()


# ============================================================
# 5. PANTALLA PRINCIPAL
# ============================================================

def mostrar_inicio(finca):
    """Muestra el panel ejecutivo de Hato La Casita."""

    # Datos de la finca
    total_vacas = finca.cantidad_vacas()
    produccion_hoy = finca.produccion_total(date.today())

    # Imágenes opcionales: se utiliza un fondo alternativo si faltan.
    foto_cabecera = imagen_base64("hato_banner.jpg")
    paisaje = imagen_base64("paisaje_fondo.jpeg")

    if not foto_cabecera[1]:
        st.warning(
            "No se encontró una imagen válida para la cabecera. "
            "Se mostrará un fondo verde."
        )

    if not paisaje[1]:
        st.info(
            "No se encontró assets/paisaje_fondo.jpeg. "
            "Los accesos rápidos utilizarán un fondo alternativo."
        )

    cargar_estilos(foto_cabecera, paisaje)

    # ---------- Resumen de la finca ----------

    st.markdown(
        '<div class="hato-section-title">Resumen de la finca</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="hato-section-subtitle">'
        'Indicadores principales de la operación.'
        '</div>',
        unsafe_allow_html=True,
    )

    col1, col2, col3 = st.columns(3, gap="medium")

    mostrar_indicador(
        col1,
        "hato-kpi-vacas",
        "logo_vaca.png",
        "",
        "Logo de vaca",
        "Vacas registradas",
        total_vacas,
        "ANIMALES",
        "🐄",
    )

    mostrar_indicador(
        col2,
        "hato-kpi-produccion",
        "logo_jarra.png",
        "",
        "Logo de jarra de leche",
        "Producción de hoy",
        produccion_hoy,
        "LITROS DE LECHE",
        "🥛",
    )

    mostrar_indicador(
        col3,
        "hato-kpi-cesped",
        "logo_cesped.png",
        "",
        "Logo de césped",
        "Estado de praderas",
        12,
        "POTREROS",
        "🌱",
    )

    # ---------- Accesos rápidos ----------

    st.divider()

    st.markdown(
        '<div class="hato-section-title">Accesos rápidos</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="hato-section-subtitle">'
        'Accede directamente a las operaciones más utilizadas.'
        '</div>',
        unsafe_allow_html=True,
    )

    col1, col2, col3 = st.columns(3, gap="medium")

    mostrar_acceso(
        col1,
        "inicio-card-produccion",
        "logo_cantina_leche.png",
        "",
        "Cantina de leche",
        "🥛",
        "Registrar producción",
        "Registra la producción de leche de tus vacas.",
        "Registrar producción",
        "inicio_ir_registrar_produccion",
        "Registrar producción",
    )

    mostrar_acceso(
        col2,
        "inicio-card-vaca",
        "cara_vaca.jpeg",
        "hato-action-logo-cow",
        "Cara de vaca",
        "🐄",
        "Registrar vaca",
        "Añade animales al inventario de la finca.",
        "Registrar vaca",
        "inicio_ir_registrar_vaca",
        "Registrar vaca",
    )

    mostrar_acceso(
        col3,
        "inicio-card-reporte",
        "logo_barras.png",
        "hato-action-logo-bars",
        "Gráfico de barras",
        "📊",
        "Reporte diario",
        "Consulta los resultados por vaca y potrero.",
        "Ver reporte diario",
        "inicio_ir_reporte_diario",
        "Reporte diario",
    )

    # ---------- Pie de pantalla ----------

    st.divider()
    st.caption("CONTROL LECHERO · HATO LA CASITA")
