# streamlit_app/components/history.py
import streamlit as st

import requests

import pandas as pd


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


def run_history():
    """
    Muestra la interfaz de historial de predicciones y maneja la lógica para
    consultar y mostrar predicciones previas por nombre de usuario.
    
    Esta función crea un componente Streamlit que:
    1. Muestra un campo para ingresar el nombre de usuario
    2. Realiza la consulta a la API al hacer clic en el botón
    3. Muestra los resultados en una tabla formateada
    
    :return: None, los resultados se muestran directamente en la interfaz Streamlit
    :rtype: None
    """
    st.header("Historial de predicciones")
    
    username_for_history = st.text_input("👤 Nombre de usuario para consultar historial")
    if st.button("Consultar historial"):
        if not username_for_history:
            st.error("Debes proporcionar un nombre de usuario")
        else:
            try:
                response = requests.get(f"{API_URL}/predict/predictions/{username_for_history}")
                if response.status_code == 200:
                    predictions = response.json()
                    
                    if not predictions:
                        st.info("No hay predicciones registradas para este usuario")
                    else:
                        st.success(f"Se encontraron {len(predictions)} predicciones")
                        
                        records = []
                        for p in predictions:
                            features = p["feature_data"]
                            records.append({
                                "Precio predicho": format_price(p["prediction"]),
                                "Área habitable (ft²)": features.get("sqft_living"),
                                "Habitaciones": features.get("bedrooms"),
                                "Baños": features.get("bathrooms"),
                                "Calidad (1-13)": features.get("grade")
                            })
                        
                        df = pd.DataFrame(records)
                        st.dataframe(df, use_container_width=True)
                else:
                    st.error(f"❌ Error al consultar historial: {response.text}")
            except Exception as e:
                st.error(f"❌ Error de conexión: {e}")
