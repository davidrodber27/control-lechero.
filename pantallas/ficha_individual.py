
import streamlit as st
import pandas as pd
import html
from datetime import date


# ==========================================================
# FUNCIONES AUXILIARES DE DISEÑO
# ==========================================================

def mostrar_tarjeta(titulo, valor, unidad="", icono="📊"):
    """
    Muestra una tarjeta con el título y el valor centrados.
    """

    titulo_seguro = html.escape(str(titulo))
    valor_seguro = html.escape(str(valor))
    unidad_segura = html.escape(str(unidad))
    icono_seguro = html.escape(str(icono))

    st.markdown(
        f"""
        <div class="ficha-kpi">
            <div class="ficha-kpi-icon">{icono_seguro}</div>
            <div class="ficha-kpi-title">{titulo_seguro}</div>
            <div class="ficha-kpi-value">{valor_seguro}</div>
            <div class="ficha-kpi-unit">{unidad_segura}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def mostrar_tarjeta_dato(titulo, valor, icono="📌"):
    """
    Tarjeta compacta para datos generales y reproductivos.
    """

    titulo_seguro = html.escape(str(titulo))
    valor_seguro = html.escape(str(valor))
    icono_seguro = html.escape(str(icono))

    st.markdown(
        f"""
        <div class="ficha-dato">
            <div class="ficha-dato-icon">{icono_seguro}</div>
            <div class="ficha-dato-title">{titulo_seguro}</div>
            <div class="ficha-dato-value">{valor_seguro}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def titulo_seccion(titulo, subtitulo=None):
    """
    Encabezado uniforme para las secciones de la ficha.
    """

    titulo_seguro = html.escape(str(titulo))

    subtitulo_html = ""

    if subtitulo:
        subtitulo_seguro = html.escape(str(subtitulo))
        subtitulo_html = (
            f'<div class="ficha-section-subtitle">'
            f'{subtitulo_seguro}</div>'
        )

    st.markdown(
        f"""
        <div class="ficha-section-title">
            {titulo_seguro}
        </div>
        {subtitulo_html}
        """,
        unsafe_allow_html=True,
    )


# ==========================================================
# FICHA INDIVIDUAL
# ==========================================================

def mostrar_ficha_individual(finca):

    # ------------------------------------------------------
    # ESTILOS VISUALES
    # ------------------------------------------------------

    st.markdown(
        """
        <style>

        .ficha-header {
            background: linear-gradient(120deg, #153D2B, #28734D);
            padding: 25px 28px;
            border-radius: 16px;
            margin-bottom: 22px;
            color: white;
        }

        .ficha-header-label {
            font-size: 0.76rem;
            font-weight: 700;
            letter-spacing: 2px;
            color: #C6E2D0;
            margin-bottom: 7px;
        }

        .ficha-header-name {
            font-size: 2rem;
            font-weight: 800;
            color: white;
            margin: 0;
            line-height: 1.2;
        }

        .ficha-header-info {
            font-size: 0.92rem;
            color: #E0F0E6;
            margin-top: 10px;
        }

        .ficha-section-title {
            font-size: 1.25rem;
            font-weight: 800;
            color: var(--text-color);
            margin-top: 10px;
            margin-bottom: 5px;
        }

        .ficha-section-subtitle {
            font-size: 0.85rem;
            color: var(--text-color);
            opacity: 0.68;
            margin-bottom: 17px;
        }

        .ficha-kpi {
            background: var(--secondary-background-color);
            border: 1px solid rgba(128, 128, 128, 0.18);
            border-radius: 14px;
            padding: 20px 10px;
            min-height: 165px;
            text-align: center;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            margin-bottom: 12px;
        }

        .ficha-kpi-icon {
            font-size: 1.55rem;
            margin-bottom: 8px;
        }

        .ficha-kpi-title {
            font-size: 0.78rem;
            font-weight: 700;
            color: var(--text-color);
            opacity: 0.75;
            min-height: 35px;
            display: flex;
            align-items: center;
            justify-content: center;
        }

        .ficha-kpi-value {
            font-size: 1.85rem;
            font-weight: 800;
            color: var(--text-color);
            line-height: 1.25;
            overflow-wrap: anywhere;
        }

        .ficha-kpi-unit {
            font-size: 0.75rem;
            font-weight: 600;
            color: var(--text-color);
            opacity: 0.62;
            margin-top: 5px;
        }

        .ficha-dato {
            background: var(--secondary-background-color);
            border: 1px solid rgba(128, 128, 128, 0.18);
            border-radius: 12px;
            padding: 17px 12px;
            min-height: 125px;
            text-align: center;
            margin-bottom: 12px;
        }

        .ficha-dato-icon {
            font-size: 1.35rem;
            margin-bottom: 5px;
        }

        .ficha-dato-title {
            font-size: 0.76rem;
            font-weight: 700;
            opacity: 0.68;
            margin-bottom: 7px;
        }

        .ficha-dato-value {
            font-size: 1.05rem;
            font-weight: 750;
            color: var(--text-color);
            overflow-wrap: anywhere;
        }

        .ficha-parent-card {
            background: var(--secondary-background-color);
            border: 1px solid rgba(128, 128, 128, 0.18);
            border-radius: 14px;
            padding: 20px;
            margin-bottom: 12px;
        }

        .ficha-parent-title {
            font-size: 1rem;
            font-weight: 800;
            margin-bottom: 13px;
            color: var(--text-color);
        }

        .ficha-parent-label {
            font-size: 0.76rem;
            font-weight: 700;
            opacity: 0.65;
            margin-top: 9px;
        }

        .ficha-parent-value {
            font-size: 0.95rem;
            font-weight: 650;
            color: var(--text-color);
            overflow-wrap: anywhere;
        }

        @media (max-width: 640px) {
            .ficha-header {
                padding: 20px;
            }

            .ficha-header-name {
                font-size: 1.55rem;
            }

            .ficha-kpi {
                min-height: 145px;
                padding: 14px 7px;
            }

            .ficha-kpi-value {
                font-size: 1.5rem;
            }

            .ficha-dato {
                min-height: 115px;
            }
        }

        </style>
        """,
        unsafe_allow_html=True,
    )

    # ------------------------------------------------------
    # ENCABEZADO PRINCIPAL
    # ------------------------------------------------------

    st.title("🐄 Ficha individual")

    st.caption(
        "Consulta la información general, reproductiva, "
        "genealógica y productiva de cada animal."
    )

    # ------------------------------------------------------
    # SELECCIÓN DE VACA
    # ------------------------------------------------------

    vacas = list(finca.vacas.values())

    if not vacas:
        st.info("No hay vacas registradas en la finca.")
        return

    opciones_vacas = {
        f"{vaca.identificacion} - {vaca.nombre}": vaca
        for vaca in vacas
    }

    seleccion = st.selectbox(
        "Selecciona una vaca:",
        options=list(opciones_vacas.keys()),
        index=None,
        placeholder="Buscar por identificación o nombre...",
    )

    if seleccion is None:
        st.info("Selecciona una vaca para consultar su ficha.")
        return

    vaca = opciones_vacas[seleccion]

    # ------------------------------------------------------
    # ENCABEZADO DE IDENTIFICACIÓN
    # ------------------------------------------------------

    nombre_seguro = html.escape(str(vaca.nombre))
    identificacion_segura = html.escape(str(vaca.identificacion))
    raza_segura = html.escape(str(vaca.raza))

    st.markdown(
        f"""
        <div class="ficha-header">
            <div class="ficha-header-label">
                HATO LA CASITA · REGISTRO INDIVIDUAL
            </div>
            <div class="ficha-header-name">
                🐄 {nombre_seguro}
            </div>
            <div class="ficha-header-info">
                Identificación: {identificacion_segura}
                &nbsp; | &nbsp;
                Raza: {raza_segura}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ------------------------------------------------------
    # DATOS GENERALES
    # ------------------------------------------------------

    st.divider()

    titulo_seccion(
        "📋 Datos generales",
        "Información de identificación y características del animal.",
    )

    fecha_nacimiento = date.fromisoformat(
        vaca.fecha_nacimiento
    )

    col1, col2, col3 = st.columns(3, gap="medium")

    with col1:
        mostrar_tarjeta_dato(
            "Nombre",
            vaca.nombre,
            "🐄",
        )

    with col2:
        mostrar_tarjeta_dato(
            "Identificación",
            vaca.identificacion,
            "🆔",
        )

    with col3:
        mostrar_tarjeta_dato(
            "Raza",
            vaca.raza,
            "🧬",
        )

    col1, col2 = st.columns(2, gap="medium")

    with col1:
        mostrar_tarjeta_dato(
            "Fecha de nacimiento",
            fecha_nacimiento.strftime("%d/%m/%Y"),
            "📅",
        )

    with col2:
        mostrar_tarjeta_dato(
            "Edad actual",
            vaca.edad_actual,
            "⏳",
        )

    # ------------------------------------------------------
    # CONTROL REPRODUCTIVO
    # ------------------------------------------------------

    st.divider()

    titulo_seccion(
        "🧬 Control reproductivo",
        "Seguimiento de partos y tiempo transcurrido desde el último parto.",
    )

    if vaca.fecha_ultimo_parto:

        fecha_parto = date.fromisoformat(
            vaca.fecha_ultimo_parto
        )

        fecha_parto_texto = fecha_parto.strftime("%d/%m/%Y")
        dias_posparto_texto = vaca.dias_posparto

    else:
        fecha_parto_texto = "Sin registro"
        dias_posparto_texto = "Sin registro"

    col1, col2, col3 = st.columns(3, gap="medium")

    with col1:
        mostrar_tarjeta_dato(
            "Número de partos",
            vaca.numero_partos,
            "🐮",
        )

    with col2:
        mostrar_tarjeta_dato(
            "Último parto",
            fecha_parto_texto,
            "📅",
        )

    with col3:
        mostrar_tarjeta_dato(
            "Días posparto",
            dias_posparto_texto,
            "⏱️",
        )

    if not vaca.fecha_ultimo_parto:
        st.info(
            "No hay fecha del último parto registrada."
        )

    # ------------------------------------------------------
    # ASCENDENCIA
    # ------------------------------------------------------

    st.divider()

    titulo_seccion(
        "🌳 Ascendencia",
        "Información genealógica registrada para este animal.",
    )

    col_madre, col_padre = st.columns(2, gap="medium")

    with col_madre:

        madre_nombre = html.escape(
            str(vaca.madre_nombre or "No registrado")
        )

        madre_raza = html.escape(
            str(vaca.madre_raza or "No registrada")
        )

        st.markdown(
            f"""
            <div class="ficha-parent-card">
                <div class="ficha-parent-title">
                    ♀ Madre
                </div>
                <div class="ficha-parent-label">Nombre</div>
                <div class="ficha-parent-value">
                    {madre_nombre}
                </div>
                <div class="ficha-parent-label">Raza</div>
                <div class="ficha-parent-value">
                    {madre_raza}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col_padre:

        padre_nombre = html.escape(
            str(vaca.padre_nombre or "No registrado")
        )

        padre_raza = html.escape(
            str(vaca.padre_raza or "No registrada")
        )

        st.markdown(
            f"""
            <div class="ficha-parent-card">
                <div class="ficha-parent-title">
                    ♂ Padre
                </div>
                <div class="ficha-parent-label">Nombre</div>
                <div class="ficha-parent-value">
                    {padre_nombre}
                </div>
                <div class="ficha-parent-label">Raza</div>
                <div class="ficha-parent-value">
                    {padre_raza}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # ------------------------------------------------------
    # PREPARACIÓN DEL HISTORIAL
    # ------------------------------------------------------

    st.divider()

    titulo_seccion(
        "📊 Análisis de producción",
        "Indicadores y comportamiento productivo de la vaca.",
    )

    registros = []

    for fecha_registro, datos in vaca.registros.items():

        litros_manana = datos.get("litros_manana")
        litros_tarde = datos.get("litros_tarde")

        total_dia = (
            (litros_manana or 0)
            + (litros_tarde or 0)
        )

        dia_completo = (
            litros_manana is not None
            and litros_tarde is not None
        )

        registros.append({
            "Fecha": pd.to_datetime(fecha_registro),
            "Mañana": litros_manana,
            "Tarde": litros_tarde,
            "Total": total_dia,
            "Día completo": dia_completo,
            "Potrero": datos.get("potrero"),
        })

    if not registros:

        st.info(
            "Esta vaca todavía no tiene registros de producción "
            "para generar estadísticas."
        )

        mostrar_tarjeta(
            "Producción acumulada",
            f"{vaca.produccion_acumulada():,}",
            "Litros",
            "🥛",
        )

        return

    df = pd.DataFrame(registros)

    df = (
        df.sort_values("Fecha")
        .reset_index(drop=True)
    )

    fecha_minima = df["Fecha"].min().date()
    fecha_maxima = df["Fecha"].max().date()

    # ------------------------------------------------------
    # FILTROS DE FECHAS
    # ------------------------------------------------------

    st.markdown("### 🗓️ Periodo de consulta")

    col_desde, col_hasta = st.columns(2, gap="medium")

    with col_desde:

        fecha_desde = st.date_input(
            "Desde",
            value=fecha_minima,
            min_value=fecha_minima,
            max_value=fecha_maxima,
            key=f"ficha_desde_{vaca.identificacion}",
        )

    with col_hasta:

        fecha_hasta = st.date_input(
            "Hasta",
            value=fecha_maxima,
            min_value=fecha_minima,
            max_value=fecha_maxima,
            key=f"ficha_hasta_{vaca.identificacion}",
        )

    if fecha_desde > fecha_hasta:

        st.error(
            "La fecha inicial no puede ser posterior "
            "a la fecha final."
        )

        return

    df_periodo = df[
        (df["Fecha"].dt.date >= fecha_desde)
        & (df["Fecha"].dt.date <= fecha_hasta)
    ].copy()

    if df_periodo.empty:

        st.warning(
            "No existen registros de producción "
            "en el periodo seleccionado."
        )

        return

    # ------------------------------------------------------
    # INDICADORES PRODUCTIVOS
    # ------------------------------------------------------

    dias_completos = df_periodo[
        df_periodo["Día completo"]
    ]

    produccion_acumulada = int(
        df_periodo["Total"].sum()
    )

    promedio_diario = (
        dias_completos["Total"].mean()
        if not dias_completos.empty
        else None
    )

    produccion_maxima = (
        int(dias_completos["Total"].max())
        if not dias_completos.empty
        else None
    )

    produccion_minima = (
        int(dias_completos["Total"].min())
        if not dias_completos.empty
        else None
    )

    dias_registrados = len(df_periodo)

    dias_incompletos = int(
        (~df_periodo["Día completo"]).sum()
    )

    # ------------------------------------------------------
    # TARJETAS DE INDICADORES DEL PERIODO
    # ------------------------------------------------------

    st.markdown("### 🏆 Indicadores del periodo")

    st.caption(
        f"Resultados entre el "
        f"{fecha_desde.strftime('%d/%m/%Y')} y "
        f"{fecha_hasta.strftime('%d/%m/%Y')}."
    )

    col1, col2, col3, col4 = st.columns(4, gap="medium")

    with col1:
        mostrar_tarjeta(
            "Producción acumulada",
            f"{produccion_acumulada:,}",
            "Litros",
            "🥛",
        )

    with col2:
        mostrar_tarjeta(
            "Promedio diario",
            (
                f"{promedio_diario:.1f}"
                if promedio_diario is not None
                else "—"
            ),
            "Litros / día",
            "📈",
        )

    with col3:
        mostrar_tarjeta(
            "Producción máxima",
            (
                produccion_maxima
                if produccion_maxima is not None
                else "—"
            ),
            "Litros / día",
            "🏆",
        )

    with col4:
        mostrar_tarjeta(
            "Producción mínima",
            (
                produccion_minima
                if produccion_minima is not None
                else "—"
            ),
            "Litros / día",
            "📉",
        )

    # ------------------------------------------------------
    # INDICADORES DE COMPLETITUD
    # ------------------------------------------------------

    st.markdown("### 📅 Estado de los registros")

    col1, col2, col3 = st.columns(3, gap="medium")

    with col1:
        mostrar_tarjeta(
            "Días registrados",
            dias_registrados,
            "Días",
            "📋",
        )

    with col2:
        mostrar_tarjeta(
            "Días completos",
            len(dias_completos),
            "Días",
            "✅",
        )

    with col3:
        mostrar_tarjeta(
            "Días incompletos",
            dias_incompletos,
            "Días",
            "⚠️",
        )

    if dias_incompletos > 0:

        st.warning(
            "Hay días con uno de los ordeños pendiente. "
            "Se contabilizan los litros registrados, pero "
            "esos días no participan en el promedio, "
            "máximo ni mínimo diario."
        )

    # ------------------------------------------------------
    # GRÁFICA DE EVOLUCIÓN POR ORDEÑO
    # ------------------------------------------------------

    st.divider()

    st.markdown("### 📈 Evolución de los ordeños")

    st.caption(
        "Comportamiento de la producción de leche "
        "durante la mañana y la tarde."
    )

    df_grafica = df_periodo.set_index("Fecha")

    st.line_chart(
        df_grafica[["Mañana", "Tarde"]],
        x_label="Fecha",
        y_label="Litros",
        height=350,
    )

    # ------------------------------------------------------
    # GRÁFICA DE PRODUCCIÓN TOTAL DIARIA
    # ------------------------------------------------------

    st.divider()

    st.markdown("### 🥛 Producción total por día")

    st.caption(
        "Litros registrados en ambos ordeños para cada fecha."
    )

    st.bar_chart(
        df_grafica[["Total"]],
        x_label="Fecha",
        y_label="Litros",
        height=300,
    )

    # ------------------------------------------------------
    # COMPARACIÓN DE ORDEÑOS
    # ------------------------------------------------------

    st.divider()

    st.markdown("### ⚖️ Comparación de ordeños")

    total_manana = int(
        df_periodo["Mañana"].sum()
    )

    total_tarde = int(
        df_periodo["Tarde"].sum()
    )

    col1, col2 = st.columns(2, gap="medium")

    with col1:
        mostrar_tarjeta(
            "Producción de mañana",
            f"{total_manana:,}",
            "Litros",
            "🌅",
        )

    with col2:
        mostrar_tarjeta(
            "Producción de tarde",
            f"{total_tarde:,}",
            "Litros",
            "🌇",
        )

    # ------------------------------------------------------
    # HISTORIAL DETALLADO
    # ------------------------------------------------------

    st.divider()

    st.markdown("### 📑 Historial de producción")

    st.caption(
        "Detalle de los registros correspondientes "
        "al periodo seleccionado."
    )

    df_tabla = df_periodo.copy()

    df_tabla["Fecha"] = (
        df_tabla["Fecha"].dt.strftime("%d/%m/%Y")
    )

    df_tabla = df_tabla.rename(
        columns={
            "Mañana": "Mañana (L)",
            "Tarde": "Tarde (L)",
            "Total": "Total (L)",
        }
    )

    df_tabla = df_tabla[
        [
            "Fecha",
            "Mañana (L)",
            "Tarde (L)",
            "Total (L)",
            "Potrero",
        ]
    ]

    st.dataframe(
        df_tabla,
        use_container_width=True,
        hide_index=True,
    )
