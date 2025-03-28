# streamlit_app/app.py
import streamlit as st

from components.prediction import run_prediction

from components.user_management import run_user_management

from components.history import run_history


st.set_page_config(
    page_title="🏠 OIC House Price Predictor",
    page_icon="🏠",
    layout="wide"
)

st.sidebar.markdown("# 🇨🇴 Observatorio Inmobiliario Catastral 🇨🇴")
st.sidebar.title("Servicios")
operation = st.sidebar.selectbox(
    "Selecciona una operación", 
    ("👤 Gestión de usuarios", "🏠 Predicción de precio", "📊 Historial de predicciones")
)

st.title("🏠 Predictor de Precios de Inmuebles de King County")

if operation == "👤 Gestión de usuarios":
    run_user_management()
    
elif operation == "🏠 Predicción de precio":
    run_prediction()

elif operation == "📊 Historial de predicciones":
    run_history()

st.markdown("---")
st.caption("© 2025 OIC House Price Predictor - Desarrollado con ❤️ en FastAPI y Streamlit")
