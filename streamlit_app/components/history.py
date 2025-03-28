# streamlit_app/components/history.py
import streamlit as st

import requests

import pandas as pd


API_URL = "http://oic-model-api:8000"


def format_price(price):
    return f"${price:,.2f}"


def run_history():
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
