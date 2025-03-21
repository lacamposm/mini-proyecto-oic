import requests

import streamlit as st

API_URL = "http://oic-model-api:8000"

st.title("🚀 OIC MODEL API 🚀")

operacion = st.sidebar.selectbox("Selecciona una operación", ("Ingreso de usuario", "Predicción"))

if operacion == "Ingreso de usuario":
    st.header("👤 Crear Usuario")
    user_name = st.text_input("Nombre de usuario")
    if st.button("Crear Usuario"):
        response = requests.post(f"{API_URL}/users/", json={"user_name": user_name})
        if response.status_code == 200:
            data = response.json()
            st.success(f"✅ Usuario creado con éxito: {data}")
        else:
            st.error(f"❌ Error al crear el usuario: {response.text}")

elif operacion == "Predicción":
    st.header("📊 Predicción")
    user_name = st.text_input("Nombre de usuario (debe ser un usuario registrado)")
    metros_cuadrados = st.number_input("Metros cuadrados", min_value=0.0, step=0.1, format="%.2f")
    num_habitaciones = st.number_input("Número de habitaciones", min_value=0, step=1)
    ubicaciones = ["Centro", "Norte", "Sur", "Este", "Oeste"]
    ubicacion = st.selectbox("Ubicación", ubicaciones)
    if st.button("Realizar Predicción"):
        payload = {
            "metros_cuadrados": metros_cuadrados,
            "num_habitaciones": num_habitaciones,
            "ubicacion": ubicacion
        }
        response = requests.post(f"{API_URL}/predict/?user_name={user_name}", json=payload)
        if response.status_code == 200:
            data = response.json()
            st.success(f"✅ La predicción para el valor de este predio es: {data['prediction']}")
        else:
            st.error(f"❌ Error al realizar la predicción: {response.text}")
