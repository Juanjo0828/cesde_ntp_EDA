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

API_BASE_URL = "https://knowly-back-10.onrender.com/usuario"

# Botón limpiar caché
if st.button("🔄 Refrescar Datos (Limpiar Caché)"):
    st.cache_data.clear()
    st.rerun()

# --- GET API ---
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

    # ✅ CAMBIO 1: Manejo de errores mejorado
    except requests.exceptions.Timeout:
        st.error("⏱️ La API tardó demasiado en responder.")
    except requests.exceptions.ConnectionError:
        st.error("🌐 No se pudo conectar con el servidor.")
    except Exception:
        st.error("❌ Error inesperado.")
    
    return pd.DataFrame()

# --- POST API ---
def post_usuario_data(data):
    try:
        response = requests.post(API_BASE_URL, json=data, timeout=10)
        if response.status_code == 200 or response.status_code == 201:
            st.success("Usuario enviado exitosamente a la API.")
            return True
        else:
            st.error(f"Error al enviar: Status {response.status_code}")
            try:
                st.json(response.json())
            except:
                st.error(response.text)
            return False
    except Exception as e:
        st.error(f"Error de conexión: {e}")
        return False

# --- Cargar datos ---
with st.spinner("Conectando con la API..."):
    df_usuario = get_api_data()

# --- Gráfica ---
st.subheader("📊 Gráfica inicial")
if not df_usuario.empty and 'rol' in df_usuario.columns:
    role_counts = df_usuario['rol'].value_counts().reset_index()
    role_counts.columns = ['Rol', 'Cantidad']
    chart = alt.Chart(role_counts).mark_bar().encode(
        x='Rol',
        y='Cantidad',
        color='Rol'
    )
    st.altair_chart(chart, use_container_width=True)
else:
    st.info("No hay datos")

# --- Crear usuario ---
st.header("➕ Crear Usuario")

with st.form("form"):
    post_id = st.text_input("ID Usuario")
    post_nombre = st.text_input("Nombre")
    post_correo = st.text_input("Correo")
    post_password = st.text_input("Contraseña", type="password")

    submit_post = st.form_submit_button("Crear Usuario")

if submit_post:
    if not post_id or not post_nombre or not post_password:
        st.error("El ID, Nombre y Contraseña son obligatorios.")

    # ✅ CAMBIO 2: Validaciones nuevas
    elif "@" not in post_correo:
        st.error("Correo inválido")
    elif len(post_password) < 6:
        st.error("La contraseña debe tener mínimo 6 caracteres")

    else:
        post_data = {
            "ideusuario": post_id,
            "nombre": post_nombre,
            "correo": post_correo,
            "contrasenia": post_password
        }

        # ✅ CAMBIO 3: Spinner UX
        with st.spinner("Enviando datos..."):
            success = post_usuario_data(post_data)

        # ✅ CAMBIO 4: Recarga automática
        if success:
            st.rerun()

# --- Info ---
st.info(f"API: {API_BASE_URL}")