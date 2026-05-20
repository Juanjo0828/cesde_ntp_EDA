import streamlit as st

# Configuración de la página
st.set_page_config(
    page_title="Plantilla de Resultados - Proyecto Analítica",
    page_icon="📝",
    layout="wide"
)

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

st.title("📝 Plantilla de Entrega: Resultados del EDA")
st.markdown("""
### Instrucciones
Utiliza esta página para documentar tus hallazgos. Completa cada sección basándote en lo que descubriste en la pestaña de **Análisis Exploratorio**.
Al finalizar, puedes previsualizar tu reporte consolidado.
""")

st.divider()

# --- Formulario de Resultados ---
with st.container():
    st.header("🔍 1. Identificación y Contexto")
    contexto = st.text_area(
        "¿De qué se trata el dataset? (Deducción del origen, tema y propósito)",
        placeholder="Este conjunto de datos contiene información sobre los programas " \
        "académicos y de ext de la Institución Universitaria Digital de Antioquia para el" \
        " periodo 2024-02. Incluye detalles como el número de estudiantes matriculados," \
        " programas académicos ofrecidos, niveles de formación (técnico, tecnológico" \
        ", profesional, posgrado)el proposito de ello es tener registro sobre toda la informacion" \
        "para tener mejor administracion de datos ",
        height=150
    )

    st.header("❗ 2. Calidad de los Datos")
    calidad = st.text_area(
        "¿Qué encontraste sobre los datos faltantes y la limpieza?",
        placeholder="Ej: Se observó que las columnas 'Numero materias inscritas," \
        " numero de materias aprobadas y estrato' tiene la misma cantidad de datos faltantes.",
        height=150
    )

    st.header("📈 3. Hallazgos Estadísticos Key")
    estadisticas = st.text_area(
        "Interpretación de los números y categorías principales (Medias, modas, etc.)",
        placeholder="La mayoria de la mediana y el minimo de escritos esta alrrededor" \
        " dl 50 porciento de la media y el minimo de laas materias aprobadas se describe " \
        "de tal manera que se inscriben 1 y el 0 porcentaje de los estudiantes deben," \
        " por lo cual muchos estudiantes incriben materias y las aprueban  y el numero de" \
        " estudiantes es alto  ",
        height=150
    )

    st.header("💡 4. Conclusión Final")
    conclusion = st.text_area(
        "¿Cuál es el mensaje principal que nos dan estos datos?",
        placeholder="El dataset revela que se encontraron 11930 registros" \
        " y 4 llaves numericas en las cuales son solo una descriptiva como un dato int y" \
        " las demas reprersentadas con texto, por lo tanto el mensaje que nos da " \
        "estos datos es que muchos estudiantes fuero admitidos en la universidad ",
        height=100
    )

st.divider()

# --- Generación de Reporte ---
if st.button("🚀 Generar Previsualización del Reporte"):
    if contexto and calidad and estadisticas and conclusion:
        st.success("✅ Reporte Generado Exitosamente")
        
        reporte_md = f"""
        # Reporte de Análisis Exploratorio de Datos
        
        ## 1. Identificación y Contexto
        {contexto}
        
        ## 2. Calidad de los Datos
        {calidad}
        
        ## 3. Hallazgos Estadísticos Clave
        {estadisticas}
        
        ## 4. Conclusión Final
        {conclusion}
        
        ---
        *Generado por el módulo de Reportes - Proyecto Integrador*
        """
        
        st.markdown(reporte_md)
        st.download_button(
            label="📥 Descargar Reporte (.md)",
            data=reporte_md,
            file_name="reporte_eda_estudiante.md",
            mime="text/markdown"
        )
    else:
        st.warning("⚠️ Por favor, completa todas las secciones antes de generar el reporte.")

# --- Barra Lateral ---
st.sidebar.info("Esta es tu hoja de trabajo. Asegúrate de analizar bien los datos antes de escribir tus conclusiones.")
st.sidebar.markdown("---")
st.sidebar.write("© 2026 - Plantilla de Resultados")
