import streamlit as st

st.set_page_config(
    page_title="Control Lechero",
    page_icon="🐄",
    layout="wide"
)

st.title("🐄 Control Lechero")
st.subheader("Hato La Casita")

st.write(
    "Bienvenido al sistema de gestión del hato "
    "y control de producción de leche."
)

st.divider()
st.header("Resumen de la finca")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Vacas registradas", 0)

with col2:
    st.metric("Producción de hoy", "0 L")

with col3:
    st.metric("Potreros", 12)

st.info(
    "Versión inicial de demostración. "
    "Los datos reales se conectarán más adelante."
)
