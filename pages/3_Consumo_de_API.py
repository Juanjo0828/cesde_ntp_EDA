import streamlit as st
import pandas as pd
import requests

# Configuración de la página
st.set_page_config(page_title="Gestión Corporativa Colombia - MockAPI", layout="wide")

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

st.title("🏢 Gestión Corporativa: Vendedores y Sucursales en Colombia")
st.markdown("""
### Objetivo
En esta sección, consumiremos **dos entidades** personalizadas creadas en **MockAPI** que simulan datos de una empresa en Colombia.
Los datos incluyen información sobre el equipo de ventas y las sedes físicas de la organización.
""")

# --- Configuración de la API (MockAPI) ---
# REEMPLAZA ESTE ID CON TU PROPIO ID DE MOCKAPI
MOCK_API_ID = "69dc251a84f912a264037197" 
# Nota: MockAPI por defecto suele crear los recursos bajo /api/v1 o directamente en la raíz.
# Según tus pruebas, la ruta directa funcionó, pero si falla con 404, prueba añadiendo /api/v1
MOCK_API_BASE_URL = f"https://{MOCK_API_ID}.mockapi.io"

# --- Botón para Limpiar Caché (En caso de errores de conexión previos) ---
if st.button("🔄 Refrescar Datos (Limpiar Caché)"):
    st.cache_data.clear()
    st.rerun()

# --- Función para obtener datos de MockAPI ---
@st.cache_data
def get_mockapi_data(entity):
    # Probamos primero la ruta directa, si falla probamos con /api/v1
    paths_to_try = [f"{MOCK_API_BASE_URL}/{entity}", f"{MOCK_API_BASE_URL}/api/v1/{entity}"]
    
    last_error = ""
    for url in paths_to_try:
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                if isinstance(data, list):
                    return pd.DataFrame(data)
                else:
                    return pd.DataFrame([data])
            else:
                last_error = f"Status {response.status_code} en {url}"
        except Exception as e:
            last_error = f"Error: {e} en {url}"
            
    st.error(f"No se pudo conectar con '{entity}'. Último intento: {last_error}")
    return pd.DataFrame()

# --- Carga de Datos ---
with st.spinner("Conectando con MockAPI..."):
    df_vendedores = get_mockapi_data("vendedores")
    df_sucursales = get_mockapi_data("sucursales")

# --- Sección 1: Gestión de Vendedores (Entidad 1) ---
st.header("👥 Equipo de Vendedores")
st.markdown("Consulta y filtra el personal de ventas de la compañía en Colombia.")

if not df_vendedores.empty:
    # Filtros integrados en el contenido
    col_v_1, col_v_2 = st.columns(2)
    
    with col_v_1:
        ciudades_v = ["Todas"] + sorted(df_vendedores['ciudad'].unique().tolist())
        sel_ciudad_v = st.selectbox("Filtrar vendedores por Ciudad:", ciudades_v, key="sel_v_ciudad")
    
    with col_v_2:
        cargos_v = ["Todos"] + sorted(df_vendedores['cargo'].unique().tolist())
        sel_cargo_v = st.selectbox("Filtrar por Cargo:", cargos_v, key="sel_v_cargo")

    # Aplicación de filtros
    f_vendedores = df_vendedores.copy()
    if sel_ciudad_v != "Todas":
        f_vendedores = f_vendedores[f_vendedores['ciudad'] == sel_ciudad_v]
    if sel_cargo_v != "Todos":
        f_vendedores = f_vendedores[f_vendedores['cargo'] == sel_cargo_v]

    # Métricas de Vendedores
    mv1, mv2, mv3 = st.columns(3)
    with mv1:
        st.metric("Total Vendedores", len(f_vendedores))
    with mv2:
        ventas = pd.to_numeric(f_vendedores['ventas_mes'], errors='coerce').fillna(0)
        st.metric("Promedio Ventas Mes", f"${ventas.mean():,.0f} COP" if not f_vendedores.empty else "N/A")
    with mv3:
        st.metric("Ventas Totales (Filtro)", f"${ventas.sum():,.0f} COP" if not f_vendedores.empty else "N/A")

    st.dataframe(f_vendedores, use_container_width=True)
else:
    st.info("💡 Esperando datos de 'vendedores'...")

st.divider()

# --- Sección 2: Sedes y Sucursales (Entidad 2) ---
st.header("📍 Sedes y Sucursales")
st.markdown("Directorio de oficinas y centros de distribución a nivel nacional.")

if not df_sucursales.empty:
    # Filtros integrados en el contenido
    col_s_1, col_s_2 = st.columns(2)
    
    with col_s_1:
        search_sede = st.text_input("Buscar sede por nombre:", "", key="search_s_nombre")
    
    with col_s_2:
        ciudades_s = ["Todas"] + sorted(df_sucursales['ciudad'].unique().tolist())
        sel_ciudad_s = st.selectbox("Filtrar sedes por Ciudad:", ciudades_s, key="sel_s_ciudad")

    # Aplicación de filtros
    f_sucursales = df_sucursales.copy()
    if search_sede:
        f_sucursales = f_sucursales[f_sucursales['nombre_sede'].str.contains(search_sede, case=False)]
    if sel_ciudad_s != "Todas":
        f_sucursales = f_sucursales[f_sucursales['ciudad'] == sel_ciudad_s]

    # Métricas de Sucursales
    ms1, ms2 = st.columns(2)
    with ms1:
        st.metric("Total Sedes Activas", len(f_sucursales))
    with ms2:
        empleados = pd.to_numeric(f_sucursales['empleados'], errors='coerce').fillna(0)
        st.metric("Personal Total en Sedes", f"{empleados.sum():,.0f} Personas" if not f_sucursales.empty else "N/A")

    st.dataframe(f_sucursales, use_container_width=True)
else:
    st.info("💡 Esperando datos de 'sucursales'...")

# --- Información Técnica ---
st.info(f"""
**Detalles de la API (MockAPI):**
- **Base URL:** `{MOCK_API_BASE_URL}`
- **Entidades:** `/vendedores` y `/sucursales`.
- **Nota:** Si sigues viendo 404, asegúrate de que los nombres de los recursos en MockAPI coincidan exactamente (sin espacios ni mayúsculas).
""")
