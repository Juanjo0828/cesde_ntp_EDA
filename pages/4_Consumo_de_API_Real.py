import streamlit as st
import pandas as pd
import requests
import altair as alt
import matplotlib.pyplot as plt

# Configuración de la página
st.set_page_config(page_title="Gestión Corporativa Colombia - API Real", layout="wide")

st.title("knowly")
st.markdown("""
### Objetivo
En esta sección, consumiremos **una entidad de usuario** personalizada que simula datos de un usuario.
Los datos incluyen información sobre la organización.
""")


# URL de la API
API_BASE_URL = "http://localhost:8080/usuario"

# --- Botón para Limpiar Caché (En caso de errores de conexión previos) ---
if st.button("🔄 Refrescar Datos (Limpiar Caché)"):
    st.cache_data.clear()
    st.rerun()

# --- Función para obtener datos de la API ---
@st.cache_data
def get_api_data():
    try:
        response = requests.get(API_BASE_URL, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if isinstance(data, list):
                return pd.DataFrame(data)
            else:
                return pd.DataFrame([data])
        else:
            st.error(f"Error: Status {response.status_code}")
            return pd.DataFrame()
    except Exception as e:
        st.error(f"Error de conexión: {e}")
        return pd.DataFrame()

# --- Función para enviar datos a la API (POST) ---
def post_usuario_data(data):
    try:
        response = requests.post(API_BASE_URL, json=data, timeout=10)
        if response.status_code == 200 or response.status_code == 201:
            st.success("Usuario enviado exitosamente a la API.")
            return True
        else:
            st.error(f"Error al enviar: Status {response.status_code}")
            return False
    except Exception as e:
        st.error(f"Error de conexión: {e}")
        return False

# --- Carga de Datos ---
with st.spinner("Conectando con la API..."):
    df_usuario = get_api_data()

# --- Sección 1: Gestión de Usuario ---
st.header("👥 Información del Usuario")
st.markdown("Datos del usuario obtenido de la API")

if not df_usuario.empty:
    # Mostrar los datos del usuario
    st.dataframe(df_usuario, use_container_width=True)
    
    # Análisis simple
    st.subheader("Análisis del Usuario")
    if len(df_usuario) == 1:
        user = df_usuario.iloc[0]
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("ID Usuario", user['ideusuario'])
        with col2:
            st.metric("Rol", user['rol'])
        with col3:
            st.metric("Nombre Completo", f"{user['nombre']} {user['apellido']}")
        
        # Más detalles
        st.markdown("**Detalles adicionales:**")
        st.write(f"Documento: {user['documento']}")
        st.write(f"Correo: {user['correo']}")
        # Nota: No mostrar contraseña por seguridad
        
        # Visualización simple con Altair
        st.subheader("Visualización de Datos del Usuario")
        # Crear un gráfico de barras para los campos de texto (longitud)
        fields = ['nombre', 'apellido', 'correo']
        lengths = [len(str(user[field])) for field in fields]
        chart_data = pd.DataFrame({'Campo': fields, 'Longitud': lengths})
        chart = alt.Chart(chart_data).mark_bar().encode(
            x='Campo',
            y='Longitud',
            color='Campo'
        ).properties(title="Longitud de Campos de Texto")
        st.altair_chart(chart, use_container_width=True)
        
    else:
        st.metric("Total de usuarios", len(df_usuario))
        st.dataframe(df_usuario, use_container_width=True)
        
        # Filtros interactivos
        st.subheader("Filtros Interactivos")
        col1, col2 = st.columns(2)
        with col1:
            roles = ["Todos"] + list(df_usuario['rol'].unique())
            selected_rol = st.selectbox("Filtrar por Rol", roles)
        with col2:
            nombres = ["Todos"] + list(df_usuario['nombre'].unique())
            selected_nombre = st.selectbox("Filtrar por Nombre", nombres)
        
        filtered_df = df_usuario.copy()
        if selected_rol != "Todos":
            filtered_df = filtered_df[filtered_df['rol'] == selected_rol]
        if selected_nombre != "Todos":
            filtered_df = filtered_df[filtered_df['nombre'] == selected_nombre]
        
        st.dataframe(filtered_df, use_container_width=True)
        
        # Visualización con Altair
        st.subheader("Distribución de Roles")
        role_counts = df_usuario['rol'].value_counts().reset_index()
        role_counts.columns = ['Rol', 'Cantidad']
        chart = alt.Chart(role_counts).mark_bar().encode(
            x='Rol',
            y='Cantidad',
            color='Rol'
        ).properties(title="Distribución de Roles de Usuarios")
        st.altair_chart(chart, use_container_width=True)
        
else:
    st.info("💡 No se pudieron obtener datos del usuario de la API.")



# --- Información Técnica ---
st.info(f"""
**Detalles de la API:**
- **URL:** `{API_BASE_URL}`
- **Métodos:** GET para obtener datos, POST para enviar usuario.
- **Nota:** Asegúrate de que el servidor esté corriendo en localhost:8080.
""")

