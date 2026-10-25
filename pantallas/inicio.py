
import streamlit as st
from datetime import date


def mostrar_inicio(finca):
    """Muestra el panel ejecutivo de Hato La Casita."""

    # ----------------------------------------------
    # 1. DATOS REALES DE LA FINCA
    # ----------------------------------------------

    total_vacas = finca.cantidad_vacas()
    produccion_hoy = finca.produccion_total(date.today())

    # ----------------------------------------------
    # 2. ESTILOS VISUALES
    # ----------------------------------------------

    st.markdown(
        """
        <style>
            /* Cabecera principal */
            .hato-hero {
                background:
                    linear-gradient(
                        90deg,
                        rgba(20, 48, 34, 0.96) 0%,
                        rgba(36, 74, 54, 0.86) 55%,
                        rgba(36, 74, 54, 0.42) 100%
                    ),
                    url("https://images.unsplash.com/photo-1500595046743-cd271d694d30?auto=format&fit=crop&w=1800&q=85");
                background-size: cover;
                background-position: center 55%;
                min-height: 230px;
                padding: 34px;
                border-radius: 18px;
                display: flex;
                flex-direction: column;
                justify-content: center;
                margin-bottom: 28px;
                box-shadow: 0 8px 24px rgba(22, 52, 35, 0.14);
            }

            .hato-eyebrow {
                color: #D5E6D6;
                font-size: 12px;
                font-weight: 700;
                letter-spacing: 2.5px;
                text-transform: uppercase;
                margin-bottom: 12px;
            }

            .hato-title {
                color: #FFFFFF;
                font-size: 38px;
                font-weight: 750;
                line-height: 1.15;
                margin: 0 0 12px 0;
            }

            .hato-description {
                color: #F0F5F0;
                font-size: 16px;
                max-width: 620px;
                line-height: 1.6;
                margin: 0;
            }

            /* Títulos de sección */
            .hato-section-title {
                color: #244A36;
                font-size: 22px;
                font-weight: 750;
                margin: 8px 0 4px 0;
            }

            .hato-section-subtitle {
                color: #69786D;
                font-size: 14px;
                margin: 0 0 18px 0;
            }

            /* Tarjetas de indicadores */
            .hato-kpi {
                background: #FFFFFF;
                border: 1px solid #E0E8E0;
                border-radius: 16px;
                padding: 22px 12px;
                min-height: 168px;
                text-align: center;
                box-shadow: 0 4px 14px rgba(28, 58, 39, 0.045);
            }

            .hato-kpi-icon {
                font-size: 27px;
                margin-bottom: 12px;
            }

            .hato-kpi-label {
                color: #647368;
                font-size: 13px;
                font-weight: 600;
                margin-bottom: 8px;
            }

            .hato-kpi-value {
                color: #244A36;
                font-size: 32px;
                font-weight: 750;
                line-height: 1.2;
            }

            .hato-kpi-unit {
                color: #647368;
                font-size: 14px;
                font-weight: 500;
            }

            /* Tarjetas de accesos rápidos */
            .hato-action-title {
                color: #244A36;
                font-size: 17px;
                font-weight: 700;
                margin-bottom: 6px;
            }

            .hato-action-description {
                color: #69786D;
                font-size: 13px;
                line-height: 1.5;
                min-height: 40px;
            }

            /* Botones de la pantalla */
            div.stButton > button {
                border-radius: 9px;
                min-height: 42px;
                font-weight: 600;
            }

            /* Ajustes para pantallas pequeñas */
            @media (max-width: 700px) {
                .hato-hero {
                    padding: 24px 20px;
                    min-height: 210px;
                }

                .hato-title {
                    font-size: 29px;
                }

                .hato-description {
                    font-size: 14px;
                }

                .hato-kpi {
                    padding: 18px 6px;
                    min-height: 150px;
                }

                .hato-kpi-value {
                    font-size: 25px;
                }
            }
        </style>
        """,
        unsafe_allow_html=True
    )

    # ----------------------------------------------
    # 3. CABECERA CON FOTOGRAFÍA DE FONDO
    # ----------------------------------------------

        # 3. CABECERA CON FOTOGRAFÍA
    st.image(
        "https://images.unsplash.com/photo-1500595046743-cd271d694d30"
        "?auto=format&fit=crop&w=1800&q=85",
        use_container_width=True,
    )

    st.markdown(
        """
        <div style="
            background-color: #244A36;
            padding: 28px;
            border-radius: 14px;
            margin-top: -8px;
            margin-bottom: 24px;
            color: white;
        ">
            <div style="
                color: #D5E6D6;
                font-size: 12px;
                font-weight: bold;
                letter-spacing: 2px;
            ">
                HATO LA CASITA · GESTIÓN GANADERA
            </div>
            <h1 style="
                color: white;
                margin: 12px 0;
                font-size: 34px;
            ">
                Control Lechero
            </h1>
            <p style="
                color: #F0F5F0;
                font-size: 16px;
                margin-bottom: 0;
            ">
                Toda la información de tu hato en un solo lugar.
                Controla la producción, administra tus animales
                y consulta el desempeño diario de tu finca.
            </p>
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
        st.markdown(
            f"""
            <div class="hato-kpi">
                <div class="hato-kpi-icon">🐄</div>
                <div class="hato-kpi-label">Vacas registradas</div>
                <div class="hato-kpi-value">{total_vacas}</div>
                <div class="hato-kpi-unit">animales</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            f"""
            <div class="hato-kpi">
                <div class="hato-kpi-icon">🥛</div>
                <div class="hato-kpi-label">Producción de hoy</div>
                <div class="hato-kpi-value">{produccion_hoy}</div>
                <div class="hato-kpi-unit">litros de leche</div>
            </div>
            """,
            unsafe_allow_html=True
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

