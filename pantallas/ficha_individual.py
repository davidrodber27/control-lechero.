
import streamlit as st
import pandas as pd
from datetime import date


def mostrar_ficha_individual(finca):

    st.title("🐄 Ficha individual")
    st.caption(
        "Información general, reproductiva, genealógica "
        "y análisis de producción."
    )

    # --------------------------------------------------
    # SELECCIÓN DE VACA
    # --------------------------------------------------

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
        placeholder="Buscar por identificación o nombre..."
    )

    if seleccion is None:
        st.info("Selecciona una vaca para consultar su ficha.")
        return

    vaca = opciones_vacas[seleccion]

    # --------------------------------------------------
    # DATOS GENERALES
    # --------------------------------------------------

    st.divider()
    st.subheader("📋 Datos generales")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Nombre", vaca.nombre)

    with col2:
        st.metric("Identificación", vaca.identificacion)

    with col3:
        st.metric("Raza", vaca.raza)

    fecha_nacimiento = date.fromisoformat(
        vaca.fecha_nacimiento
    )

    st.write(
        "**Fecha de nacimiento:**",
        fecha_nacimiento.strftime("%d/%m/%Y")
    )

    st.write("**Edad actual:**", vaca.edad_actual)

    # --------------------------------------------------
    # CONTROL REPRODUCTIVO
    # --------------------------------------------------

    st.divider()
    st.subheader("🧬 Control reproductivo")

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Número de partos",
            vaca.numero_partos
        )

    with col2:
        if vaca.fecha_ultimo_parto:
            st.metric(
                "Días posparto",
                vaca.dias_posparto
            )
        else:
            st.metric("Días posparto", "Sin registro")

    if vaca.fecha_ultimo_parto:

        fecha_parto = date.fromisoformat(
            vaca.fecha_ultimo_parto
        )

        st.write(
            "**Último parto:**",
            fecha_parto.strftime("%d/%m/%Y")
        )

    else:
        st.info("No hay fecha del último parto registrada.")

    # --------------------------------------------------
    # ASCENDENCIA
    # --------------------------------------------------

    st.divider()
    st.subheader("🌳 Ascendencia")

    col_madre, col_padre = st.columns(2)

    with col_madre:

        st.markdown("### Madre")

        st.write(
            "**Nombre:**",
            vaca.madre_nombre or "No registrado"
        )

        st.write(
            "**Raza:**",
            vaca.madre_raza or "No registrada"
        )

    with col_padre:

        st.markdown("### Padre")

        st.write(
            "**Nombre:**",
            vaca.padre_nombre or "No registrado"
        )

        st.write(
            "**Raza:**",
            vaca.padre_raza or "No registrada"
        )

    # --------------------------------------------------
    # PREPARACIÓN DEL HISTORIAL
    # --------------------------------------------------

    st.divider()
    st.subheader("📊 Análisis de producción")

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
            "Potrero": datos.get("potrero")
        })

    if not registros:

        st.info(
            "Esta vaca todavía no tiene registros de producción "
            "para generar estadísticas."
        )

        st.metric(
            "Producción acumulada",
            f"{vaca.produccion_acumulada()} L"
        )

        return

    df = pd.DataFrame(registros)
    df = df.sort_values("Fecha").reset_index(drop=True)

    fecha_minima = df["Fecha"].min().date()
    fecha_maxima = df["Fecha"].max().date()

    # --------------------------------------------------
    # FILTROS DE FECHAS
    # --------------------------------------------------

    st.markdown("### 🗓️ Periodo de consulta")

    col_desde, col_hasta = st.columns(2)

    with col_desde:

        fecha_desde = st.date_input(
            "Desde",
            value=fecha_minima,
            min_value=fecha_minima,
            max_value=fecha_maxima,
            key=f"ficha_desde_{vaca.identificacion}"
        )

    with col_hasta:

        fecha_hasta = st.date_input(
            "Hasta",
            value=fecha_maxima,
            min_value=fecha_minima,
            max_value=fecha_maxima,
            key=f"ficha_hasta_{vaca.identificacion}"
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

    # --------------------------------------------------
    # INDICADORES PRODUCTIVOS
    # --------------------------------------------------

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

    dias_incompletos = (
        ~df_periodo["Día completo"]
    ).sum()

    st.markdown("### 🏆 Indicadores del periodo")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Producción acumulada",
            f"{produccion_acumulada:,} L"
        )

    with col2:
        st.metric(
            "Promedio diario",
            (
                f"{promedio_diario:.1f} L"
                if promedio_diario is not None
                else "Sin datos"
            )
        )

    with col3:
        st.metric(
            "Producción máxima",
            (
                f"{produccion_maxima} L"
                if produccion_maxima is not None
                else "Sin datos"
            )
        )

    with col4:
        st.metric(
            "Producción mínima",
            (
                f"{produccion_minima} L"
                if produccion_minima is not None
                else "Sin datos"
            )
        )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Días registrados", dias_registrados)

    with col2:
        st.metric(
            "Días completos",
            len(dias_completos)
        )

    with col3:
        st.metric(
            "Días incompletos",
            int(dias_incompletos)
        )

    if dias_incompletos > 0:

        st.warning(
            "Hay días con uno de los ordeños pendiente. "
            "Se contabilizan los litros registrados, pero "
            "esos días no participan en el promedio, "
            "máximo ni mínimo diario."
        )

    # --------------------------------------------------
    # GRÁFICA DE EVOLUCIÓN POR ORDEÑO
    # --------------------------------------------------

    st.divider()
    st.markdown("### 📈 Evolución de los ordeños")

    df_grafica = df_periodo.set_index("Fecha")

    st.line_chart(
        df_grafica[["Mañana", "Tarde"]],
        x_label="Fecha",
        y_label="Litros",
        height=350
    )

    # --------------------------------------------------
    # GRÁFICA DE PRODUCCIÓN TOTAL DIARIA
    # --------------------------------------------------

    st.divider()
    st.markdown("### 🥛 Producción total por día")

    st.bar_chart(
        df_grafica[["Total"]],
        x_label="Fecha",
        y_label="Litros",
        height=300
    )

    # --------------------------------------------------
    # COMPARACIÓN DE ORDEÑOS
    # --------------------------------------------------

    st.divider()
    st.markdown("### ⚖️ Comparación de ordeños")

    total_manana = int(
        df_periodo["Mañana"].sum()
    )

    total_tarde = int(
        df_periodo["Tarde"].sum()
    )

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Producción de mañana",
            f"{total_manana:,} L"
        )

    with col2:
        st.metric(
            "Producción de tarde",
            f"{total_tarde:,} L"
        )

    # --------------------------------------------------
    # HISTORIAL DETALLADO
    # --------------------------------------------------

    st.divider()
    st.markdown("### 📑 Historial de producción")

    df_tabla = df_periodo.copy()

    df_tabla["Fecha"] = (
        df_tabla["Fecha"].dt.strftime("%d/%m/%Y")
    )

    df_tabla = df_tabla.rename(
        columns={
            "Mañana": "Mañana (L)",
            "Tarde": "Tarde (L)",
            "Total": "Total (L)"
        }
    )

    df_tabla = df_tabla[
        [
            "Fecha",
            "Mañana (L)",
            "Tarde (L)",
            "Total (L)",
            "Potrero"
        ]
    ]

    st.dataframe(
        df_tabla,
        use_container_width=True,
        hide_index=True
    )

