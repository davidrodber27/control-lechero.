
import streamlit as st
from datetime import date

from modelos.vaca import Vaca
from modelos.control_lechero import ControlLechero
from servicios.persistencia import cargar_vacas


def mostrar_registrar_vaca(finca, supabase):

    st.title("Registrar una vaca")

    st.write(
        "Registra la identificación y los datos "
        "generales y reproductivos de cada animal."
    )

    # --------------------------------------------------
    # 1. FORMULARIO
    # --------------------------------------------------

    with st.form("formulario_vaca"):

        st.subheader("Datos generales")

        identificacion = st.text_input(
            "Identificación de la vaca",
            placeholder="Ejemplo: V001"
        )

        nombre = st.text_input(
            "Nombre de la vaca",
            placeholder="Ejemplo: Roja"
        )

        opciones_razas = [
            "Holstein",
            "Jersey",
            "Normando",
            "Ayrshire",
            "Cruce",
            "Otra"
        ]

        raza_seleccionada = st.selectbox(
            "Raza",
            opciones_razas
        )

        raza_personalizada = st.text_input(
            "Especificar raza o cruce (si aplica)",
            placeholder="Ejemplo: Holstein x Jersey"
        )

        fecha_nacimiento = st.date_input(
            "Fecha de nacimiento",
            value=date.today(),
            max_value=date.today(),
            format="DD/MM/YYYY"
        )

        st.divider()
        st.subheader("Datos reproductivos")

        tiene_partos = st.checkbox(
            "La vaca ya ha tenido partos"
        )

        if tiene_partos:

            numero_partos = st.number_input(
                "Número de partos registrados",
                min_value=1,
                value=1,
                step=1
            )

            fecha_ultimo_parto = st.date_input(
                "Fecha del último parto",
                value=None,
                min_value=fecha_nacimiento,
                max_value=date.today(),
                format="DD/MM/YYYY"
            )

        else:
            numero_partos = 0
            fecha_ultimo_parto = None

        enviar = st.form_submit_button(
            "Registrar vaca"
        )

    # --------------------------------------------------
    # 2. PROCESAR EL FORMULARIO
    # --------------------------------------------------

    if not enviar:
        return

    identificacion_limpia = identificacion.strip().upper()
    nombre_limpio = nombre.strip()
    raza_personalizada_limpia = raza_personalizada.strip()

    # Determinar la raza
    if raza_seleccionada in ("Cruce", "Otra"):
        raza = raza_personalizada_limpia
    elif raza_personalizada_limpia:
        raza = raza_personalizada_limpia
    else:
        raza = raza_seleccionada

    # --------------------------------------------------
    # 3. VALIDACIONES
    # --------------------------------------------------

    if not identificacion_limpia:
        st.error("Debes escribir la identificación de la vaca.")
        return

    if not nombre_limpio:
        st.error("Debes escribir el nombre de la vaca.")
        return

    if not raza:
        st.error("Debes seleccionar o escribir la raza de la vaca.")
        return

    if tiene_partos and fecha_ultimo_parto is None:
        st.error("Debes seleccionar la fecha del último parto.")
        return

    if finca.buscar_vaca(identificacion_limpia):
        st.error("Ya existe una vaca con esa identificación.")
        return

    # --------------------------------------------------
    # 4. CREAR EL OBJETO VACA
    # --------------------------------------------------

    try:

        nueva_vaca = Vaca(
            nombre=nombre_limpio,
            fecha_nacimiento=fecha_nacimiento,
            raza=raza,
            identificacion=identificacion_limpia,
            fecha_ultimo_parto=fecha_ultimo_parto,
            numero_partos=int(numero_partos)
        )

    except Exception as error:
        st.error("No fue posible crear el registro de la vaca.")
        st.caption("Detalle técnico:")
        st.code(str(error))
        return

    # --------------------------------------------------
    # 5. COMPROBAR SI YA EXISTE EN SUPABASE
    # --------------------------------------------------

    try:

        consulta = (
            supabase
            .table("vacas")
            .select("identificacion")
            .eq("identificacion", identificacion_limpia)
            .execute()
        )

        if consulta.data:

            st.warning(
                "Esta identificación ya existe en Supabase. "
                "No se realizará un segundo registro."
            )

            # Recuperar los datos existentes
            finca_actualizada = ControlLechero(
                finca.nombre_finca
            )

            finca_actualizada = cargar_vacas(
                supabase=supabase,
                finca=finca_actualizada,
                cargar_historial=True
            )

            st.session_state.finca = finca_actualizada
            st.rerun()

            return

    except Exception as error:
        st.error("No fue posible comprobar la identificación en Supabase.")
        st.caption("Detalle técnico:")
        st.code(str(error))
        return

    # --------------------------------------------------
    # 6. PREPARAR LOS DATOS PARA SUPABASE
    # --------------------------------------------------

    datos_vaca = {
        "identificacion": identificacion_limpia,
        "nombre": nombre_limpio,
        "raza": raza,
        "fecha_nacimiento": fecha_nacimiento.isoformat(),
        "fecha_ultimo_parto": (
            fecha_ultimo_parto.isoformat()
            if fecha_ultimo_parto is not None
            else None
        ),
        "numero_partos": int(numero_partos)
    }

    # --------------------------------------------------
    # 7. GUARDAR EN SUPABASE
    # --------------------------------------------------

    try:

        respuesta = (
            supabase
            .table("vacas")
            .insert(datos_vaca)
            .execute()
        )

        if not respuesta.data:
            st.error(
                "Supabase no confirmó el registro. "
                "Verifica la tabla antes de volver a intentarlo."
            )
            return

    except Exception as error:
        st.error("No fue posible guardar la vaca en Supabase.")
        st.caption("Detalle técnico:")
        st.code(str(error))
        return

    # --------------------------------------------------
    # 8. RECARGAR LOS ANIMALES DESDE SUPABASE
    # --------------------------------------------------

    try:

        finca_actualizada = ControlLechero(
            finca.nombre_finca
        )

        finca_actualizada = cargar_vacas(
            supabase=supabase,
            finca=finca_actualizada,
            cargar_historial=True
        )

        # Actualizar la finca guardada en la sesión
        st.session_state.finca = finca_actualizada

        st.success(
            f"¡Vaca {nombre_limpio} registrada correctamente!"
        )

        st.rerun()

    except Exception as error:

        st.error(
            "La vaca quedó guardada en Supabase, "
            "pero no fue posible actualizar la lista de la aplicación."
        )

        st.caption("Detalle técnico:")
        st.code(str(error))

