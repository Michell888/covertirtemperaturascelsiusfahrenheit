# app.py
import sys
import traceback

# Intentamos importar streamlit y si falla mostramos el error en la salida estándar
try:
    import streamlit as st
except Exception as e:
    print("ERROR: no se pudo importar streamlit.", file=sys.stderr)
    traceback.print_exc()
    raise

# --- Funciones de conversión ---
def celsius_a_fahrenheit(c: float) -> float:
    return c * 9.0 / 5.0 + 32.0

def fahrenheit_a_celsius(f: float) -> float:
    return (f - 32.0) * 5.0 / 9.0

# --- Interfaz principal dentro de una función (para atrapar errores en tiempo de ejecución) ---
def main():
    # set_page_config debe ser la primera llamada a st.* de la UI
    st.set_page_config(page_title="Conversor °C ↔ °F", page_icon="🌡", layout="centered")

    try:
        st.title("Conversor de temperaturas — Celsius ↔ Fahrenheit")
        st.write("Convierte valores entre Celsius y Fahrenheit. La app está pensada para ser robusta y fácil de desplegar.")

        modo = st.radio("Modo de conversión", ("Celsius → Fahrenheit", "Fahrenheit → Celsius"))

        # controles y resultado en dos columnas
        col_input, col_result = st.columns([2, 1])

        with col_input:
            if modo == "Celsius → Fahrenheit":
                c = st.number_input("Temperatura (°C)", value=0.0, step=0.1, format="%.2f", key="c_input")
                decimales = st.slider("Decimales a mostrar", 0, 6, 2)
                # conversión reactiva (también puedes usar un botón si prefieres)
                f = celsius_a_fahrenheit(c)
                resultado_text = f"{f:.{decimales}f} °F"
            else:
                f = st.number_input("Temperatura (°F)", value=32.0, step=0.1, format="%.2f", key="f_input")
                decimales = st.slider("Decimales a mostrar", 0, 6, 2)
                c = fahrenheit_a_celsius(f)
                resultado_text = f"{c:.{decimales}f} °C"

        with col_result:
            st.metric(label="Resultado", value=resultado_text)

        st.markdown("---")
        with st.expander("Ejemplos y equivalencias"):
            st.write("-40 °C → -40 °F (igual en ambos sistemas)")
            st.write("0 °C → 32 °F (congelación del agua)")
            st.write("100 °C → 212 °F (ebullición del agua)")

        with st.expander("Información técnica / Depuración"):
            st.write("Versión de Streamlit detectada:", st._version_)
            st.write("Si la aplicación aparece en blanco, revisa la sección 'Lista de comprobaciones' abajo.")
            st.write("Valores actuales (útiles para depurar):")
            st.json({"modo": modo, "c": locals().get("c", None), "f": locals().get("f", None), "decimales": decimales})

        st.caption("Hecho con ❤ — asegúrate de que el archivo se llame app.py y no streamlit.py")

    except Exception:
        st.error("Se produjo un error en la ejecución de la app. Revisa el traceback en la salida abajo:")
        st.text(traceback.format_exc())
        # re-lanzamos por si quieres ver el log en la terminal/Cloud
        raise

if _name_ == "_main_":
    main()
