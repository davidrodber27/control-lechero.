import streamlit as st
from datetime import date
import base64
import mimetypes
from pathlib import Path


def mostrar_inicio(finca):
    """Muestra el panel ejecutivo de Hato La Casita."""

    # ----------------------------------------------
    # 1. DATOS REALES DE LA FINCA
    # ----------------------------------------------

    total_vacas = finca.cantidad_vacas()
    produccion_hoy = finca.produccion_total(date.today())

    
    # ----------------------------------------------
    # 2. ESTILOS VISUALES Y CABECERA
    # ----------------------------------------------

    ruta_foto = (
        Path(__file__).resolve().parent.parent
        / "assets"
        / "hato_banner.jpg"
    )

    if not ruta_foto.is_file():
        st.error(
            "No se encontró la fotografía. Revisa que exista "
            "el archivo assets/hato_banner.jpg en GitHub."
        )
    else:
        tipo_imagen, _ = mimetypes.guess_type(str(ruta_foto))

        if tipo_imagen not in ("image/jpeg", "image/png", "image/webp"):
            st.error("La fotografía debe ser JPG, PNG o WEBP.")
        else:
            foto_codificada = base64.b64encode(
                ruta_foto.read_bytes()
            ).decode("utf-8")

            
            st.markdown(
                f"""
                <style>
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
                                rgba(12, 43, 29, 0.42),
                                rgba(12, 43, 29, 0.16),
                                rgba(12, 43, 29, 0.00)
                            ),
                            url("data:{tipo_imagen};base64,{foto_codificada}");
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
            
                    /* Estilo general de las tarjetas */
                    .hato-kpi {{
                        background: #FFFFFF;
                        border: 1px solid #E0E8E0;
                        border-radius: 16px;
                        padding: 22px 12px;
                        min-height: 168px;
                        text-align: center;
                        box-shadow: 0 4px 14px rgba(28, 58, 39, 0.045);
                        box-sizing: border-box;
                    }}
            
                    /* Tarjeta personalizada: Vacas registradas */
                    .hato-kpi-vacas {{
                        background: linear-gradient(
                            145deg,
                            #F7FCF8 0%,
                            #EDF7F0 100%
                        );
                        border: 1px solid #D9EADF;
                        border-radius: 20px;
                        padding: 26px 20px 22px;
                        min-height: 300px;
                        text-align: center;
                        box-shadow: 0 5px 18px rgba(36, 90, 58, 0.07);
                        box-sizing: border-box;
                    }}
            
                    /* Círculo verde degradado */
                    .hato-kpi-vacas .hato-kpi-icon-circle {{
                        width: 76px;
                        height: 76px;
                        margin: 0 auto 20px;
                        border-radius: 50%;
                        background: linear-gradient(
                            145deg,
                            #78B88B 0%,
                            #287849 55%,
                            #174D32 100%
                        );
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        box-shadow:
                            0 6px 14px rgba(34, 105, 65, 0.22),
                            inset 0 1px 2px rgba(255, 255, 255, 0.3);
                    }}
            
                    /* Logo dentro del círculo */
                    .hato-kpi-vacas .hato-kpi-cow-logo {{
                        width: 43px;
                        height: 43px;
                        object-fit: contain;
                        filter: brightness(0) invert(1);
                    }}
            
                    /* Icono alternativo si no se encuentra el logo */
                    .hato-kpi-vacas .hato-kpi-fallback {{
                        font-size: 36px;
                        line-height: 1;
                    }}
            
                    /* Título de la tarjeta de vacas */
                    .hato-kpi-vacas .hato-kpi-label {{
                        color: #28583C;
                        font-size: 1.18rem;
                        font-weight: 700;
                        line-height: 1.4;
                        margin-bottom: 10px;
                    }}
            
                    /* Cantidad de vacas */
                    .hato-kpi-vacas .hato-kpi-value {{
                        color: #174D32;
                        font-size: 2.8rem;
                        font-weight: 800;
                        line-height: 1.15;
                        margin: 4px 0 12px;
                        letter-spacing: -1px;
                    }}
            
                    /* Línea divisoria */
                    .hato-kpi-vacas .hato-kpi-divider {{
                        width: 54px;
                        height: 2px;
                        border-radius: 2px;
                        background: #A6CDB1;
                        margin: 0 auto 10px;
                    }}
            
                    /* Texto inferior */
                    .hato-kpi-vacas .hato-kpi-unit {{
                        color: #63836D;
                        font-size: 0.72rem;
                        font-weight: 700;
                        letter-spacing: 2px;
                        line-height: 1.4;
                    }}
            
                    /* Estilos generales de las otras tarjetas */
                    .hato-kpi-icon {{
                        font-size: 27px;
                        margin-bottom: 12px;
                    }}

                    
                    /* Tarjeta azul: Producción de hoy */
                    .hato-kpi-produccion {
                        background: linear-gradient(
                            145deg,
                            #F7FBFF 0%,
                            #EAF3FC 100%
                        );
                        border: 1px solid #D5E5F5;
                        border-radius: 20px;
                        padding: 26px 20px 22px;
                        min-height: 300px;
                        text-align: center;
                        box-shadow: 0 5px 18px rgba(35, 86, 145, 0.07);
                        box-sizing: border-box;
                    }
                    
                    /* Círculo azul degradado */
                    .hato-kpi-produccion .hato-kpi-produccion-icon-circle {
                        width: 76px;
                        height: 76px;
                        margin: 0 auto 20px;
                        border-radius: 50%;
                        background: linear-gradient(
                            145deg,
                            #78B4E8 0%,
                            #2878BE 55%,
                            #164A7A 100%
                        );
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        box-shadow:
                            0 6px 14px rgba(36, 104, 169, 0.22),
                            inset 0 1px 2px rgba(255, 255, 255, 0.3);
                    }
                    
                    /* Logo blanco dentro del círculo */
                    .hato-kpi-produccion .hato-kpi-jarra-logo {
                        width: 43px;
                        height: 43px;
                        object-fit: contain;
                        filter: brightness(0) invert(1);
                    }
                    
                    /* Icono alternativo si falta el archivo */
                    .hato-kpi-produccion .hato-kpi-jarra-fallback {
                        font-size: 36px;
                        line-height: 1;
                    }
                    
                    /* Título */
                    .hato-kpi-produccion .hato-kpi-produccion-label {
                        color: #245581;
                        font-size: 1.18rem;
                        font-weight: 700;
                        line-height: 1.4;
                        margin-bottom: 10px;
                    }
                    
                    /* Litros producidos */
                    .hato-kpi-produccion .hato-kpi-produccion-value {
                        color: #164A7A;
                        font-size: 2.8rem;
                        font-weight: 800;
                        line-height: 1.15;
                        margin: 4px 0 12px;
                        letter-spacing: -1px;
                    }
                    
                    /* Línea divisoria */
                    .hato-kpi-produccion .hato-kpi-produccion-divider {
                        width: 54px;
                        height: 2px;
                        border-radius: 2px;
                        background: #A7CBEA;
                        margin: 0 auto 10px;
                    }
                    
                    /* Unidad */
                    .hato-kpi-produccion .hato-kpi-produccion-unit {
                        color: #6485A5;
                        font-size: 0.72rem;
                        font-weight: 700;
                        letter-spacing: 2px;
                        line-height: 1.4;
                    }
                    
                    /* Adaptación para móviles */
                    @media (max-width: 700px) {
                        .hato-kpi-produccion {
                            padding: 22px 12px;
                            min-height: 280px;
                        }
                    
                        .hato-kpi-produccion .hato-kpi-produccion-label {
                            font-size: 1rem;
                        }
                    
                        .hato-kpi-produccion .hato-kpi-produccion-value {
                            font-size: 2.4rem;
                        }
                    }

            
                    .hato-kpi-label {{
                        color: #647368;
                        font-size: 13px;
                        font-weight: 600;
                        margin-bottom: 8px;
                    }}
            
                    .hato-kpi-value {{
                        color: #244A36;
                        font-size: 32px;
                        font-weight: 750;
                        line-height: 1.2;
                    }}
            
                    .hato-kpi-unit {{
                        color: #647368;
                        font-size: 14px;
                        font-weight: 500;
                    }}
            
                    .hato-action-title {{
                        color: #244A36;
                        font-size: 17px;
                        font-weight: 700;
                        margin-bottom: 6px;
                    }}
            
                    .hato-action-description {{
                        color: #69786D;
                        font-size: 13px;
                        line-height: 1.5;
                        min-height: 40px;
                    }}
            
                    div.stButton > button {{
                        border-radius: 9px;
                        min-height: 42px;
                        font-weight: 600;
                    }}
            
                    /* Adaptación para móviles */
                    @media (max-width: 700px) {{
                        .hato-hero {{
                            padding: 24px 20px;
                            min-height: 210px;
                        }}
            
                        .hato-hero-title {{
                            font-size: 30px !important;
                        }}
            
                        .hato-hero-description {{
                            font-size: 14px !important;
                        }}
            
                        .hato-kpi {{
                            padding: 18px 6px;
                            min-height: 150px;
                        }}
            
                        .hato-kpi-value {{
                            font-size: 25px;
                        }}
            
                        .hato-kpi-vacas {{
                            padding: 22px 12px;
                            min-height: 280px;
                        }}
            
                        .hato-kpi-vacas .hato-kpi-value {{
                            font-size: 2.4rem;
                        }}
            
                        .hato-kpi-vacas .hato-kpi-label {{
                            font-size: 1rem;
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



    # ----------------------------------------------
    # 4. INDICADORES CENTRADOS
    # ----------------------------------------------

    st.markdown(
        '<div class="hato-section-title">'
        'Resumen de la finca'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="hato-section-subtitle">'
        'Indicadores principales de la operación.'
        '</div>',
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns(3, gap="medium")

    
    with col1:
        ruta_logo_vaca = (
            Path(__file__).resolve().parent.parent
            / "assets"
            / "logo_vaca.png"
        )
    
        if ruta_logo_vaca.is_file():
            with open(ruta_logo_vaca, "rb") as archivo:
                logo_vaca_base64 = base64.b64encode(
                    archivo.read()
                ).decode("utf-8")
    
            logo_html = (
                f'<img src="data:image/png;base64,{logo_vaca_base64}" '
                'alt="Logo de vaca" '
                'class="hato-kpi-cow-logo" />'
            )
        else:
            logo_html = '<span class="hato-kpi-fallback">🐄</span>'
    
        tarjeta_vacas_html = f"""
        <div class="hato-kpi hato-kpi-vacas">
            <div class="hato-kpi-icon-circle">
                {logo_html}
            </div>
            <div class="hato-kpi-label">Vacas registradas</div>
            <div class="hato-kpi-value">{total_vacas}</div>
            <div class="hato-kpi-divider"></div>
            <div class="hato-kpi-unit">ANIMALES</div>
        </div>
        """
    
        st.markdown(
            tarjeta_vacas_html,
            unsafe_allow_html=True,
        )


    
    with col2:
        ruta_logo_jarra = (
            Path(__file__).resolve().parent.parent
            / "assets"
            / "logo_jarra.png"
        )
    
        if ruta_logo_jarra.is_file():
            with open(ruta_logo_jarra, "rb") as archivo:
                logo_jarra_base64 = base64.b64encode(
                    archivo.read()
                ).decode("utf-8")
    
            logo_html = (
                f'<img src="data:image/png;base64,{logo_jarra_base64}" '
                'alt="Logo de jarra de leche" '
                'class="hato-kpi-jarra-logo" />'
            )
        else:
            logo_html = '<span class="hato-kpi-jarra-fallback">🥛</span>'
    
        tarjeta_produccion_html = f"""
        <div class="hato-kpi hato-kpi-produccion">
            <div class="hato-kpi-produccion-icon-circle">
                {logo_html}
            </div>
    
            <div class="hato-kpi-produccion-label">
                Producción de hoy
            </div>
    
            <div class="hato-kpi-produccion-value">
                {produccion_hoy}
            </div>
    
            <div class="hato-kpi-produccion-divider"></div>
    
            <div class="hato-kpi-produccion-unit">
                LITROS DE LECHE
            </div>
        </div>
        """
    
        st.markdown(
            tarjeta_produccion_html,
            unsafe_allow_html=True,
        )


    with col3:
        st.markdown(
            """
            <div class="hato-kpi">
                <div class="hato-kpi-icon">🌱</div>
                <div class="hato-kpi-label">Potreros</div>
                <div class="hato-kpi-value">12</div>
                <div class="hato-kpi-unit">potreros configurados</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    # ----------------------------------------------
    # 5. ACCESOS RÁPIDOS
    # ----------------------------------------------

    st.divider()

    st.markdown(
        '<div class="hato-section-title">'
        'Accesos rápidos'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="hato-section-subtitle">'
        'Accede directamente a las operaciones más utilizadas.'
        '</div>',
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns(3, gap="medium")

    with col1:
        with st.container(border=True):
            st.markdown("### 🥛")
            st.markdown(
                '<div class="hato-action-title">'
                'Registrar producción'
                '</div>',
                unsafe_allow_html=True
            )
            st.markdown(
                '<div class="hato-action-description">'
                'Registra la producción de leche de tus vacas.'
                '</div>',
                unsafe_allow_html=True
            )

            if st.button(
                "Registrar producción",
                key="inicio_ir_registrar_produccion",
                use_container_width=True
            ):
                st.session_state.pagina = "Registrar producción"
                st.rerun()

    with col2:
        with st.container(border=True):
            st.markdown("### ♟")
            st.markdown(
                '<div class="hato-action-title">'
                'Registrar vaca'
                '</div>',
                unsafe_allow_html=True
            )
            st.markdown(
                '<div class="hato-action-description">'
                'Añade animales al inventario de la finca.'
                '</div>',
                unsafe_allow_html=True
            )

            if st.button(
                "Registrar vaca",
                key="inicio_ir_registrar_vaca",
                use_container_width=True
            ):
                st.session_state.pagina = "Registrar vaca"
                st.rerun()

    with col3:
        with st.container(border=True):
            st.markdown("### ▥")
            st.markdown(
                '<div class="hato-action-title">'
                'Reporte diario'
                '</div>',
                unsafe_allow_html=True
            )
            st.markdown(
                '<div class="hato-action-description">'
                'Consulta los resultados por vaca y potrero.'
                '</div>',
                unsafe_allow_html=True
            )

            if st.button(
                "Ver reporte diario",
                key="inicio_ir_reporte_diario",
                use_container_width=True
            ):
                st.session_state.pagina = "Reporte diario"
                st.rerun()

    # ----------------------------------------------
    # 6. PIE DE PANTALLA
    # ----------------------------------------------

    st.divider()

    st.caption(
        "CONTROL LECHERO · HATO LA CASITA"
    )

