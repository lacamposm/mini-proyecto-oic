# streamlit_app/components/prediction.py
import streamlit as st

import requests

API_URL = "http://oic-model-api:8000"

def format_price(price):
    return f"${price:,.2f}"

def run_prediction():
    st.header("Predice el precio de un inmueble.")
    
    with st.form("prediction_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            user_name = st.text_input("👤 Nombre de usuario (debe estar registrado)")
            bedrooms = st.slider("🛏️ Habitaciones", 0, 10, 3)
            bathrooms = st.slider("🚿 Baños", 0.0, 10.0, 2.0, 0.25)
            sqft_living = st.number_input("📏 Área habitable (pies²)", 500, 10000, 1500)
            sqft_lot = st.number_input("🌳 Área del terreno (pies²)", 500, 100000, 5000)
            floors = st.slider("🏢 Pisos", 1.0, 4.0, 1.0, 0.5)
            waterfront = st.checkbox("🌊 Vista al mar", False)
        
        with col2:
            view = st.slider("👁️ Calidad de la vista (0-4)", 0, 4, 0)
            condition = st.slider("🔨 Condición (1-5)", 1, 5, 3)
            grade = st.slider("🏆 Calidad de construcción (1-13)", 1, 13, 7)
            renovated = st.number_input("🔄 Predio renovado (0 si no aplica)", 0, 1, 0)
            zipcode = st.text_input("📮 Código ZIP", "98178")
            lat = st.number_input("📍 Latitud", 47.0, 48.0, 47.5, 0.001)
            long = st.number_input("📍 Longitud", -123.0, -121.0, -122.2, 0.001)
        
        submit_button = st.form_submit_button("Predecir precio")
    
    if submit_button:
        if not user_name:
            st.error("⚠️ Debes ingresar un nombre de usuario válido")
        else:
            with st.spinner("⏳ Calculando predicción..."):
                try:
                    prediction_data = {
                        "user_name": user_name,
                        "bedrooms": bedrooms,
                        "bathrooms": bathrooms,
                        "sqft_living": sqft_living,
                        "sqft_lot": sqft_lot,
                        "sqft_above": sqft_living,
                        "sqft_basement": 0,
                        "floors": floors,
                        "waterfront": str(1 if waterfront else 0),
                        "view": str(view),
                        "condition": condition,
                        "grade": grade,
                        "renovated": renovated,
                        "zipcode": zipcode,
                        "lat": lat,
                        "long": long
                    }
                    
                    response = requests.post(f"{API_URL}/predict/predict", json=prediction_data)
                    
                    if response.status_code == 200:
                        data = response.json()
                        predicted_price = data.get("predicted_price", 0)
                        
                        st.success("✅ Predicción exitosa!")
                        st.metric(label="Precio estimado de la casa", value=format_price(predicted_price))
                        
                        st.subheader("Factores principales que influyen en esta predicción:")
                        col1, col2, col3, col4 = st.columns(4)
                        col1.metric("Área habitable", f"{sqft_living} ft²")
                        col2.metric("Habitaciones", bedrooms)
                        col3.metric("Baños", bathrooms)
                        col4.metric("Calidad", f"{grade}/13")
                    else:
                        st.error(f"❌ Error: {response.text}")
                        with st.expander("Detalles técnicos"):
                            st.code(
                                f"URL: {API_URL}/predict/predict\n"
                                f"Código de estado: {response.status_code}\n"
                                f"Respuesta: {response.text}"
                            )
                except Exception as e:
                    st.error(f"❌ Error de conexión: {e}")
