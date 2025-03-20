import requests

import streamlit as st

API_URL = "http://oic-model-api:8000"

st.title("Crear Usuario - OIC API")

user_name = st.text_input("Nombre de usuario")

if st.button("Crear Usuario"):

    response = requests.post(f"{API_URL}/users/", json={"user_name": user_name})

    if response.status_code == 200:
        data = response.json()
        st.success(f"Usuario creado con éxito: {data}")
    else:
        st.error(f"Error al crear el usuario: {response.text}")
