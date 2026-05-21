import streamlit as st
import pandas as pd
import requests
import altair as alt
import matplotlib.pyplot as plt

# Configuración de la página
st.set_page_config(page_title="Gestión Corporativa Colombia - API Real", layout="wide")

# --- Estilo Personalizado ---
st.markdown("""
    <style>
    .main {
        background-color: #F3E5F5;
    }
    [data-testid="stSidebar"] {
        background-color: #F3E5F5;
    }
    .stButton > button {
        background-color: #E1BEE7;
        color: #4A148C;
        border-radius: 10px;
        border: 1px solid #9C27B0;
        transition: all 0.3s;
    }
    .stButton > button:hover {
        background-color: #9C27B0;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("knowly")
st.markdown("""
### Objetivo
En esta sección, consumiremos **una entidad de usuario** personalizada que simula datos de un usuario.
Los datos incluyen información sobre la organización.
""")


# URL de la API
API_BASE_URL = "https://knowly-back-10.onrender.com/usuario"

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
            try:
                # Mostramos el detalle del error que devuelve la API (ej: "correo inválido")
                st.json(response.json())
            except:
                st.error(response.text)
            return False
    except Exception as e:
        st.error(f"Error de conexión: {e}")
        return False



# --- Carga de Datos ---
with st.spinner("Conectando con la API..."):
    df_usuario = get_api_data()

# --- Gráfica Inicial ---
st.subheader("📊 Gráfica inicial de datos obtenidos")
if not df_usuario.empty:
    if 'rol' in df_usuario.columns:
        role_counts = df_usuario['rol'].value_counts().reset_index()
        role_counts.columns = ['Rol', 'Cantidad']
        chart = alt.Chart(role_counts).mark_bar().encode(
            x='Rol',
            y='Cantidad',
            color='Rol'
        ).properties(title='Distribución inicial de Roles de Usuario')
        st.altair_chart(chart, use_container_width=True)
    else:
        st.info('No hay campo "rol" para graficar. No se muestran tablas por configuración visual.')
else:
    st.info('💡 No se pudieron obtener datos para la gráfica inicial.')

# --- Sección 1: Gestión de Usuario ---
st.header("👥 Información del Usuario")
st.markdown("Datos del usuario obtenido de la API")

if not df_usuario.empty:
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
        
        c1, c2 = st.columns(2)
        with c1:
            st.metric("Documento", user['documento'])
        with c2:
            st.metric("Correo Electrónico", user['correo'])
            
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
        # --- Panel de Filtros y Gráficos Interactivos ---
        st.subheader("🎯 Panel de Análisis y Filtros Dinámicos")
        st.markdown("Usa los controles para segmentar la información y ver las métricas actualizadas.")

        col_f1, col_f2, col_f3 = st.columns([1, 1, 1])
        with col_f1:
            roles_disponibles = sorted(list(df_usuario['rol'].unique()))
            selected_roles = st.multiselect("🎭 Seleccionar Roles:", roles_disponibles, default=roles_disponibles)
        with col_f2:
            search_term = st.text_input("🔍 Buscar por Nombre/Apellido:", placeholder="Ej: Luis")
        with col_f3:
            doc_prefix = st.text_input("🔢 Documento inicia con:", placeholder="Ej: 98")

        filtered_df = df_usuario.copy()
        
        # Aplicar Filtros Dinámicos
        if selected_roles:
            filtered_df = filtered_df[filtered_df['rol'].isin(selected_roles)]
        if doc_prefix:
            filtered_df = filtered_df[filtered_df['documento'].fillna('').astype(str).str.startswith(doc_prefix)]
        if search_term:
            mask = (
                filtered_df['nombre'].str.contains(search_term, case=False) | 
                filtered_df['apellido'].str.contains(search_term, case=False) |
                filtered_df['correo'].str.contains(search_term, case=False)
            )
            filtered_df = filtered_df[mask]
        
        # Métricas de la selección actual
        m1, m2, m3 = st.columns(3)
        
        m2.metric("🏢 Total en Base de Datos", len(df_usuario))
        m3.metric("🏷️ Roles Distintos", filtered_df['rol'].nunique() if not filtered_df.empty else 0)

        # Visualización Avanzada
        if not filtered_df.empty:
            st.subheader("📊 Análisis Gráfico de la Selección")
            col_chart1, col_chart2, col_chart3 = st.columns(3)
            
            with col_chart1:
                st.write("**Proporción por Rol**")
                role_dist = filtered_df['rol'].value_counts().reset_index()
                role_dist.columns = ['Rol', 'Cantidad']
                chart_pie = alt.Chart(role_dist).mark_arc(innerRadius=50).encode(
                    theta='Cantidad', color='Rol', tooltip=['Rol', 'Cantidad']
                ).properties(height=300)
                st.altair_chart(chart_pie, use_container_width=True)
            
            with col_chart2:
                st.write("** Nombres**")
                name_counts = filtered_df['nombre'].value_counts().head(5).reset_index()
                name_counts.columns = ['Nombre', 'Frecuencia']
                chart_names = alt.Chart(name_counts).mark_bar().encode(
                    x='Frecuencia', y=alt.Y('Nombre', sort='-x'), color='Nombre', tooltip=['Nombre', 'Frecuencia']
                ).properties(height=300)
                st.altair_chart(chart_names, use_container_width=True)

        
else:
    st.info("💡 No se pudieron obtener datos del usuario de la API.")

# --- Sección POST: Crear Usuario ---
st.header("➕ Crear Nuevo Usuario")
st.markdown("Envía los datos de un nuevo usuario a la API usando el método POST")
with st.form("post_usuario_form"):
    post_id = st.text_input("ID Usuario", placeholder="Ej: 0009")
    post_rol = st.text_input("Rol", placeholder="Ej: ESTUDIANTE")
    post_nombre = st.text_input("Nombre", placeholder="Ej: Luis")
    post_apellido = st.text_input("Apellido", placeholder="Ej: Ramírez")
    post_documento = st.text_input("Documento", placeholder="Ej: 987654321")
    post_correo = st.text_input("Correo", placeholder="Ej: luisra@gmail.edu.com")
    post_password = st.text_input("Contraseña", type="password")
    submit_post = st.form_submit_button("Crear Usuario (POST)")

if submit_post:
    if not post_id or not post_nombre or not post_password:
        st.error("El ID, Nombre y Contraseña son campos obligatorios.")
    else:
        post_data = {
            "ideusuario": post_id,
            "rol": post_rol,
            "nombre": post_nombre,
            "apellido": post_apellido,
            "documento": post_documento,
            "correo": post_correo,
            "contrasenia": post_password
        }
        post_usuario_data(post_data)




# --- Información Técnica ---
st.info(f"""
**Detalles de la API:**
- **URL:** `{API_BASE_URL}`
- **Métodos:** GET para obtener datos, POST para enviar usuario, PUT para actualizar usuario.
- **Nota:** Asegúrate de que el servidor esté corriendo en localhost:8080.
""")
