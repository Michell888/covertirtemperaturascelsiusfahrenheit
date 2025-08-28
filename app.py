import streamlit as st
import sys
import traceback

# Debe ser la PRIMERA llamada a Streamlit en el archivo
st.set_page_config(page_title="Convertidor °C → °F", page_icon="🌡", layout="centered")

def c_to_f(celsius: float) -> float:
    """Convierte Celsius a Fahrenheit."""
    return (celsius * 9.0 / 5.0) + 32.0

def main():
    st.title("🌡 Convertidor de Celsius → Fahrenheit")
    st.write("Fórmula: °F = (°C × 9/5) + 32")

    # inicializar estado de sesión
    if "historial" not in st.session_state:
        st.session_state.historial = []

    # Inputs siempre visibles (evita que la interfaz "desaparezca")
    celsius = st.number_input("Temperatura (°C)", value=0.0, step=0.1, format="%.2f")
    decimales = st.slider("Decimales a mostrar", min_value=0, max_value=6, value=2)

    # Botón de conversión (no usamos st.form para reducir potenciales confusiones)
    if st.button("Convertir"):
        try:
            fahrenheit = c_to_f(celsius)
            st.session_state.historial.append((celsius, fahrenheit))
            st.success(f"{celsius:.{decimales}f} °C = {fahrenheit:.{decimales}f} °F")
        except Exception:
            st.error("Ocurrió un error durante la conversión.")
            st.exception(traceback.format_exc())

    # Mostrar resultado más destacado (si hay historial, mostrar último)
    if st.session_state.historial:
        ult_c, ult_f = st.session_state.historial[-1]
        st.metric(label="Último resultado (°F)", value=f"{ult_f:.{decimales}f}")

    # Historial
    if st.session_state.historial:
        st.subheader("Historial de conversiones")
        rows = [{"°C": round(c, decimales), "°F": round(f, decimales)} for c, f in st.session_state.historial]
        st.table(rows)

        if st.button("Borrar historial"):
            st.session_state.historial = []
            st.experimental_rerun()

    # Panel de diagnóstico (oculto por defecto)
    with st.expander("Diagnóstico (oculto)"):
        st.write(f"Python: {sys.version.splitlines()[0]}")
        st.write(f"Streamlit: {st._version_}")

if _name_ == "_main_":
    main()
