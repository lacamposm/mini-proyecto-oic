# streamlit_app/components/prediction.py
import folium

import requests

import streamlit as st

from streamlit_folium import st_folium


API_URL = "http://oic-model-api:8000"

def format_price(price):
    """
    Formatea un valor numérico como un precio en formato monetario.
    
    :param price: El valor numérico a formatear
    :type price: float
    :return: String con formato de precio ($X,XXX.XX)
    :rtype: str
    """
    return f"${price:,.2f}"

def run_prediction():
    """
    Crea y muestra una interfaz para predecir precios de inmuebles.
    
    Esta función genera un formulario de Streamlit que:
    1. Recolecta los datos del inmueble a través de controles interactivos (sliders, inputs)
    2. Permite que el usuario ingrese las áreas en metros cuadrados (m²), 
       y se convierten a pies cuadrados (ft²) para enviarlas a la API 
       (1 m² = 10.7639 ft²)
    3. Permite seleccionar la ubicación mediante un mapa interactivo
    4. Envía los datos al API para realizar la predicción
    5. Muestra el resultado de la predicción con formato monetario
    6. Presenta métricas clave que influyen en el precio
    
    :return: None, los resultados se muestran directamente en la interfaz Streamlit
    :rtype: None
    """
    st.header("Predice el precio de un inmueble.")
    
    with st.form("prediction_form"):
        
        col1, col2 = st.columns(2)
    
        with col1:
            user_name = st.text_input("👤 Nombre de usuario (debe estar registrado)")
            area_m2 = st.number_input("📏 Área habitable en la superficie (m²)", min_value=27.0, max_value=1000.0, value=60.0, step=20.0)
            lot_area_m2 = st.number_input("🌳 Área del terreno (m²)", min_value=54.0, max_value=165136.0, value=100.0, step=100.0)
            basement_area_m2 = st.number_input("🌳 Área del sotano (m²)", min_value=0.0, max_value=50.0, value=0.0, step=1.0)

            bedrooms = st.slider("🛏️ Habitaciones", 0, 10, 3)
            bathrooms = st.slider("🚿 Baños", 0.0, 10.0, 2.0, 0.25)
            floors = st.slider("🏢 Pisos", 1.0, 4.0, 1.0, 0.5)
            waterfront = st.checkbox("🌊 Vista al mar", False)
        
        with col2:
            view = st.slider("👁️ Calidad de la vista (0-4)", 0, 4, 0)
            condition = st.slider("🔨 Condición (1-5)", 1, 5, 3)
            grade = st.slider("🏆 Calidad de construcción (1-13)", 1, 13, 7)
            renovated = st.number_input("🔄 Predio renovado (0 si no aplica)", 0, 1, 0)
            zipcode = st.text_input("📮 Código ZIP", "98178")
    
        st.markdown("### Selecciona la ubicación en el mapa")
        m = folium.Map(location=[47.5, -122.2], zoom_start=10)
        m.add_child(folium.LatLngPopup())
        folium.Marker([47.5, -122.2], tooltip="Ubicación seleccionada").add_to(m)
        map_data = st_folium(m, width=700, height=450)
        
        if map_data and map_data.get("last_clicked"):
            lat = map_data["last_clicked"].get("lat", 47.5)
            long = map_data["last_clicked"].get("lng", -122.2)
        else:
            lat = st.number_input("📍 Latitud", 47.0, 48.0, 47.5, 0.001)
            long = st.number_input("📍 Longitud", -123.0, -121.0, -122.2, 0.001)
    
        submit_button = st.form_submit_button("Predecir precio")

    if submit_button:
        if not user_name:
            st.error("⚠️ Debes ingresar un nombre de usuario válido")
        else:
            
            sqft_lot = int(round(lot_area_m2 * 10.7639))
            sqft_above = int(round(area_m2 * 10.7639))
            sqft_basement = int(round(basement_area_m2 * 10.7639))            
            sqft_living = sqft_above + sqft_basement           
            
            with st.spinner("⏳ Calculando predicción..."):
                try:
                    prediction_data = {
                        "user_name": user_name,
                        "bedrooms": bedrooms,
                        "bathrooms": bathrooms,
                        "sqft_living": sqft_living,
                        "sqft_lot": sqft_lot,
                        "sqft_above": sqft_above,
                        "sqft_basement": sqft_basement,
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
                        col1.metric("Área habitable", f"{area_m2:.2f} m²")
                        col2.metric("Área del terreno", f"{lot_area_m2:.2f} m²")
                        col3.metric("Habitaciones", bedrooms)
                        col4.metric("Baños", bathrooms)
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
                    