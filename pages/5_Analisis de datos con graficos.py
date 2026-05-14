import streamlit as st
import pandas as pd
import plotly.express as px

# Configuración de la página
st.set_page_config(page_title="Actividad: Descubriendo los Datos reales ", layout="wide")

st.title("🧩 Actividad: ¿De qué se tratan estos datos?")
st.markdown("""
### Objetivo de la Actividad
hacer filtros de los datos extraidos de internet que son reales 
""")

# --- Barra Lateral con Instrucciones e Interactividad ---
with st.container():
    st.header("📋 Guía para el analisis")
    st.info("""
    1. **Observa** los gráficos. ¿Qué tendencias aparecen?
    2. **Compara** entre columnas numéricas y categóricas.
    3. **Ajusta** cuántos registros quieres ver en las visualizaciones.
    4. **Reflexiona** sobre el contexto: fechas, municipios, valores monetarios, etc.
    """)
    
    st.markdown("---")
    uploaded_file = st.file_uploader("Sube un archivo CSV para investigar", type="csv")

    rows_to_plot = st.slider(
        "¿Cuántos registros quieres graficar?",
        min_value=5,
        max_value=100,
        value=20,
        step=5,
    )

@st.cache_data
def load_data(file):
    try:
        return pd.read_csv(file)
    except Exception as e:
        st.error(f"Error al cargar el archivo: {e}")
        return None

# Lógica de selección de archivo
df = None
if uploaded_file is not None:
    df = load_data(uploaded_file)
    if df is not None:
        st.success(" Dataset cargado para el analisis")

if df is not None:
    num_cols = df.select_dtypes(include=['number']).columns.tolist()
    cat_cols = df.select_dtypes(exclude=['number']).columns.tolist()
    rows_to_plot = min(rows_to_plot, len(df))

    with st.expander("🔧 Opciones de Gráficos", expanded=True):
        st.write("Selecciona qué columnas quieres incluir en las visualizaciones:")
        selected_numeric = st.multiselect("Columnas numéricas", num_cols, default=num_cols[:2])
        selected_categorical = st.multiselect("Columnas categóricas", cat_cols, default=cat_cols[:1])

    # --- Paso 1: Primer Impacto ---
    st.header("Step 1: 🔍 Primer Impacto (Inspección Visual)")
    st.markdown("Observa la composición del dataset y los primeros patrones en las columnas seleccionadas.")

    if selected_numeric:
        st.subheader("Tendencias en columnas numéricas")
        fig = px.line(df.head(rows_to_plot), y=selected_numeric, markers=True)
        fig.update_layout(height=400, legend_title_text='Columnas')
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Selecciona al menos una columna numérica para ver tendencias en los datos.")

    if selected_categorical:
        st.subheader("Frecuencias de categorías principales")
        for col in selected_categorical:
            counts = df[col].value_counts().head(10).reset_index()
            counts.columns = [col, 'frecuencia']
            fig = px.bar(counts, x=col, y='frecuencia', title=f"Top 10 de {col}")
            fig.update_layout(xaxis_title=col, yaxis_title='Frecuencia', height=400)
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Selecciona al menos una columna categórica para ver distribuciones.")

    # --- Paso 2: La Estructura ---
    st.header("Step 2: 🏗️ La Estructura")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Filas totales", f"{df.shape[0]}")
        st.metric("Columnas totales", f"{df.shape[1]}")
    with col2:
        st.metric("Columnas numéricas", f"{len(num_cols)}")
        st.metric("Columnas categóricas", f"{len(cat_cols)}")
    with col3:
        dtype_counts = df.dtypes.astype(str).value_counts().reset_index()
        dtype_counts.columns = ['Tipo', 'Cantidad']
        dtype_fig = px.bar(dtype_counts, x='Tipo', y='Cantidad', title='Tipos de datos en el dataset')
        dtype_fig.update_layout(height=400, xaxis_title='Tipo de dato', yaxis_title='Cantidad')
        st.plotly_chart(dtype_fig, use_container_width=True)

    with st.expander("💡 ¿Cómo interpretar la estructura?", expanded=False):
        st.write("""
        - **Filas:** Cada registro puede representar un evento, una persona, un reporte o una transacción.
        - **Columnas:** Cada característica describe un aspecto distinto del fenómeno.
        - **Tipos de datos:** Si hay muchas columnas `object`, probablemente haya nombres, códigos o ubicaciones.
        """)

    # --- Paso 3: Calidad y Vacíos ---
    st.header("Step 3: ❗ Calidad y Vacíos")
    missing = df.isnull().sum()
    missing = missing[missing > 0]
    if not missing.empty:
        st.subheader("Columnas con valores faltantes")
        missing_fig = px.bar(missing.reset_index(), x='index', y=missing.name, title='Valores faltantes por columna')
        missing_fig.update_layout(height=400, xaxis_title='Columna', yaxis_title='Cantidad de nulos')
        st.plotly_chart(missing_fig, use_container_width=True)
        st.markdown("💡 *Pregunta: ¿Por qué crees que faltan datos en esas columnas específicas?*")
    else:
        st.success("este dataset está completo,No faltan datos.")

    with st.expander("💡 ¿Qué significan los datos faltantes?", expanded=False):
        st.write("""
        - **Nulos (NaN):** Indican valores que no se recolectaron o no aplican.
        - **Impacto:** Un gran número de nulos en columnas clave puede deformar las conclusiones.
        - **Sesgo:** Si solo faltan datos para ciertos grupos, el análisis puede estar parcializado.
        """)

    # --- Paso 4: El Corazón de los Datos ---
    st.header("Step 4: 📈 El Corazón de los Datos")

    if selected_numeric:
        st.subheader("Análisis cuantitativo")
        stats = df[selected_numeric].describe().transpose()[['mean', '50%', 'std', 'min', 'max']]
        st.markdown("**Resumen estadístico de las columnas numéricas seleccionadas**")
        stats_fig = px.bar(stats.reset_index(), x='index', y=['mean', 'std'], barmode='group', title='Media y desviación estándar')
        stats_fig.update_layout(xaxis_title='Columna', yaxis_title='Valor', height=450)
        st.plotly_chart(stats_fig, use_container_width=True)

        st.markdown(f"**Tendencia de los primeros {rows_to_plot} registros**")
        trend_fig = px.line(df.head(rows_to_plot), y=selected_numeric, markers=True)
        trend_fig.update_layout(height=450, legend_title_text='Columnas')
        st.plotly_chart(trend_fig, use_container_width=True)
    else:
        st.info("Selecciona columnas numéricas para ver los gráficos cuantitativos.")

    if selected_categorical:
        st.subheader("Análisis cualitativo")
        for col in selected_categorical:
            st.markdown(f"**Distribución de '{col}'**")
            counts = df[col].value_counts().head(10).reset_index()
            counts.columns = [col, 'frecuencia']
            fig = px.bar(counts, x=col, y='frecuencia', title=f"Top 10 de {col}")
            fig.update_layout(height=400, xaxis_title=col, yaxis_title='Frecuencia')
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Selecciona columnas categóricas para ver los gráficos cualitativos.")

    # --- Conclusiones de Investigación ---
    st.header("📝 Resumen del analisis")
    st.markdown(f"""
    ### 🕵️ Informe del Detective
    Basado en tu investigación, aquí hay una validación de lo que has encontrado:
    * **Volumen**: Estás manejando **{df.shape[0]} registros**.
    * **Variables**: El dataset contiene **{len(cat_cols)} columnas de texto** y **{len(num_cols)} columnas numéricas**.
    * **Análisis visual**: Usa los gráficos interactivos para comparar tendencias en los primeros **{rows_to_plot} registros**.
    """)
else:
    st.warning("sube un archivo CSV para hacer el analisis como tal ")

