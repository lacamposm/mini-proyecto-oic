# streamlit_app/components/user_management.py
import streamlit as st

import requests


API_URL = "http://oic-model-api:8000"


def run_user_management():
    """
    """
    st.header("Gestión de usuarios")
    
    tab1, tab2, tab3 = st.tabs(["Crear usuario", "Actualizar usuario", "Eliminar usuario"])
    
    # Tab 1: Crear usuario
    with tab1:
        with st.form("create_user_form"):
            new_username = st.text_input("Nombre de nuevo usuario")
            submit_create = st.form_submit_button("Crear usuario")
        
        if submit_create:
            if not new_username:
                st.error("El nombre de usuario no puede estar vacío")
            else:
                try:
                    response = requests.post(f"{API_URL}/users/", json={"user_name": new_username})
                    
                    if response.status_code == 200:
                        user_data = response.json()
                        st.success("✅ Usuario creado exitosamente!")
                        st.json(user_data)
                    else:
                        st.error(f"❌ Error al crear usuario: {response.text}")
                except Exception as e:
                    st.error(f"❌ Error de conexión: {e}")
                    
    # Tab 2: Actualizar usuario
    with tab2:
        with st.form("update_user_form"):
            st.info("Ingresa el ID y el nuevo nombre del usuario")
            user_id = st.text_input("ID del usuario")
            updated_name = st.text_input("Nuevo nombre de usuario")
            submit_update = st.form_submit_button("Actualizar usuario")
        
        if submit_update:
            if not user_id or not updated_name:
                st.error("Todos los campos son requeridos")
            else:
                try:
                    response = requests.patch(f"{API_URL}/users/{user_id}", json={"user_name": updated_name})
                    
                    if response.status_code == 200:
                        updated_data = response.json()
                        st.success("✅ Usuario actualizado exitosamente!")
                        st.json(updated_data)
                    else:
                        st.error(f"❌ Error al actualizar usuario: {response.text}")
                except Exception as e:
                    st.error(f"❌ Error de conexión: {e}")
    
    # Tab 3: Eliminar usuario
    with tab3:
        with st.form("delete_user_form"):
            st.warning("⚠️ Esta acción eliminará al usuario y todas sus predicciones")
            delete_id = st.text_input("ID del usuario a eliminar")
            confirm = st.checkbox("Confirmo que deseo eliminar este usuario")
            submit_delete = st.form_submit_button("Eliminar usuario")
        
        if submit_delete:
            if not delete_id:
                st.error("Debes proporcionar un ID de usuario")
            elif not confirm:
                st.error("Debes confirmar la eliminación")
            else:
                try:
                    response = requests.delete(f"{API_URL}/users/{delete_id}")
                    
                    if response.status_code == 200:
                        st.success("✅ Usuario eliminado exitosamente!")
                    else:
                        st.error(f"❌ Error al eliminar usuario: {response.text}")
                except Exception as e:
                    st.error(f"❌ Error de conexión: {e}")
