

import streamlit as st
from datetime import date


def mostrar_inicio(finca):
    """Muestra el panel principal de Control Lechero."""

    # ----------------------------------------------
    # 1. DATOS PRINCIPALES
    # ----------------------------------------------

    total_vacas = finca.cantidad_vacas()
    produccion_hoy = finca.produccion_total(date.today())

    # ----------------------------------------------
    # 2. ESTILOS DE LA PANTALLA DE INICIO
    # ----------------------------------------------

    st.markdown(
        """
        <style>
            .inicio-hero {
                background: linear-gradient(
                    120deg,
                    #244A36 0%,
                    #37664A 100%
                );
                padding: 30px;
                border-radius: 16px;
                margin-bottom: 24px;
                color: white;
            }

            .inicio-etiqueta {
                font-size: 12px;
                text-transform: uppercase;
                letter-spacing: 2px;
                color: #D8E8D9;
                font-weight: 600;
                margin-bottom: 10px;
            }

            .inicio-titulo {
                font-size: 32px;
                font-weight: 700;
                color: white;
                line-height: 1.2;
                margin-bottom: 12px;
            }

            .inicio-descripcion {
                font-size: 16px;
                color: #EDF4EE;
                margin-bottom: 0;
            }

            .inicio-seccion {
                color: #244A36;
                font-size: 21px;
                font-weight: 700;
                margin-top: 8px;
                margin-bottom: 4px;
            }

            .inicio-ayuda {
                color: #647368;
                font-size: 14px;
                margin-bottom: 16px;
            }
        </style>
        """,
        unsafe_allow_html=True
    )

    # ----------------------------------------------
    # 3. ENCABEZADO PRINCIPAL
    # ----------------------------------------------

    st.markdown(
        """
        <div class="inicio-hero">
            <div class="inicio-etiqueta">
                GESTIÓN GANADERA · CONTROL LECHERO
            </div>
            <div class="inicio-titulo">
                Hato La Casita
            </div>
            <p class="inicio-descripcion">
                Bienvenido al centro de control de tu finca.
                Consulta la producción y administra tu hato
                desde un solo lugar.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # ----------------------------------------------
    # 4. INDICADORES PRINCIPALES
    # ----------------------------------------------

    st.markdown(
        '<div class="inicio-seccion">Resumen de la finca</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="inicio-ayuda">'
        'Indicadores correspondientes al estado actual de la finca.'
        '</div>',
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        with st.container(border=True):
            st.metric(
                label="🐄 Vacas registradas",
                value=total_vacas,
                help="Número de vacas registradas en el sistema."
            )

    with col2:
        with st.container(border=True):
            st.metric(
                label="🥛 Producción de hoy",
                value=f"{produccion_hoy} L",
                help="Litros registrados para la fecha actual."
            )

    with col3:
        with st.container(border=True):
            st.metric(
                label="🌱 Potreros",
                value=12,
                help="Número de potreros configurados actualmente."
            )

    # ----------------------------------------------
    # 5. ACCESOS RÁPIDOS
    # ----------------------------------------------

    st.divider()

    st.markdown(
        '<div class="inicio-seccion">Accesos rápidos</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="inicio-ayuda">'
        'Selecciona una operación para continuar.'
        '</div>',
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        with st.container(border=True):
            st.markdown("### 🥛")
            st.markdown("**Registrar producción**")
            st.caption(
                "Registra los litros de leche de cada vaca."
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
            st.markdown("### 🐄")
            st.markdown("**Registrar una vaca**")
            st.caption(
                "Incorpora un animal nuevo al inventario."
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
            st.markdown("### 📊")
            st.markdown("**Consultar reporte diario**")
            st.caption(
                "Consulta la producción por vaca y potrero."
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
