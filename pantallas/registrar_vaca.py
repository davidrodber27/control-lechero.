
import streamlit as st
from datetime import date

from modelos.vaca import Vaca


def mostrar_registrar_vaca(finca, supabase):

    st.title("Registrar una vaca")

    st.write(
        "Registra la identificación y los datos "
        "generales y reproductivos de cada animal."
    )

    with st.form("formulario_vaca"):

        # 1. Datos generales
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
            max_value=date.today()
        )

        # 2. Datos reproductivos
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


        enviar = st.form_submit_button("Registrar vaca")

    # 3. Procesar el formulario
    if enviar:

        identificacion_limpia = identificacion.strip().upper()
        nombre_limpio = nombre.strip()

        # Determinar la raza
        if raza_seleccionada in ("Cruce", "Otra"):
            raza = raza_personalizada.strip()
        elif raza_personalizada.strip():
            raza = raza_personalizada.strip()
        else:
            raza = raza_seleccionada

        # Validaciones
        if not identificacion_limpia:
            st.error("Debes escribir la identificación de la vaca.")

        elif not nombre_limpio:
            st.error("Debes escribir el nombre de la vaca.")

        elif not raza:
            st.error("Debes seleccionar o escribir la raza de la vaca.")

        elif tiene_partos and fecha_ultimo_parto is None:
            st.error("Debes seleccionar la fecha del último parto.")

        elif finca.buscar_vaca(identificacion_limpia):
            st.error("Ya existe una vaca con esa identificación.")

        

        else:

            try:
                # Crear el objeto Vaca
                nueva_vaca = Vaca(
                    nombre=nombre_limpio,
                    fecha_nacimiento=fecha_nacimiento,
                    raza=raza,
                    identificacion=identificacion_limpia,
                    fecha_ultimo_parto=fecha_ultimo_parto,
                    numero_partos=int(numero_partos)
                )
                st.write("Tipo del objeto:", type(nueva_vaca))
                st.write("Clase Vaca importada:", Vaca)
                st.write(
                    "¿Es una instancia de Vaca?",
                    isinstance(nueva_vaca, Vaca)
                )

                # Preparar datos para Supabase
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

                # Guardar en Supabase
                respuesta = (
                    supabase
                    .table("vacas")
                    .insert(datos_vaca)
                    .execute()
                )

                registros_guardados = respuesta.data

                if not registros_guardados:
                    st.error(
                        "No se confirmó el registro en Supabase. "
                        "Verifica la tabla antes de volver a intentarlo."
                    )

                else:
                    agregada = finca.agregar_vaca(nueva_vaca)

                    if agregada:
                        st.success(
                            f"Vaca {nueva_vaca.nombre} "
                            "registrada correctamente."
                        )

                        st.write(
                            f"Identificación: {nueva_vaca.identificacion}"
                        )

                        st.write(
                            f"Número de partos: {nueva_vaca.numero_partos}"
                        )

                        if nueva_vaca.dias_posparto is not None:
                            st.write(
                                f"Días posparto: "
                                f"{nueva_vaca.dias_posparto}"
                            )
                        else:
                            st.info("Esta vaca aún no tiene partos registrados.")

                    else:
                        st.warning(
                            "La vaca se guardó en Supabase, "
                            "pero no se agregó a la memoria de la aplicación. "
                            "No vuelvas a registrarla todavía."
                        )

            except Exception as error:
                st.error("No fue posible completar el registro.")
                st.caption("Detalle técnico del error:")
                st.code(str(error))

