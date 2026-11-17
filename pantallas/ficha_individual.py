
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

  
