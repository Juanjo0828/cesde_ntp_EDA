#  PROYECTO INTEGRADOR - KNOWLY

**Knowly** Es una plataforma interactiva de analítica de datos orientada al sector EdTech, diseñada para transformar la experiencia de aprendizaje y enseñar a convertir información cruda en decisiones estratégicas. Orientada a profesores, estudiantes y entornos corporativos, la app web redefine la gestión educativa a través de tres pilares tecnológicos:

**Ecosistema de Aprendizaje Colaborativo:** Un entorno bifuncional tipo Platzi que permite a los estudiantes avanzar en rutas de conocimiento personalizadas y a los profesores administrar contenidos curriculares con facilidad.

**Analítica Exploratoria y Visualización Avanzada:** Paneles dinámicos que procesan datos de rendimiento académico, transformando horas de estudio y calificaciones en gráficos interactivos que muestran el progreso real y las áreas de mejora.

**Consumo Robusto de APIs:** Gestión automatizada de usuarios, roles, seguridad y métricas corporativas mediante la integración de servicios web eficientes, garantizando una plataforma escalable y fluida.

##  Tecnologías y Librerías Importadas

Para el desarrollo de este ecosistema, se utilizaron las siguientes librerías de Python:

*   **`streamlit`**: Es el framework principal utilizado para construir la interfaz web. Permite que el análisis de datos sea interactivo y accesible desde un navegador.
*   **`pandas`**: La herramienta fundamental para la manipulación de datos. Se usa para leer archivos CSV, filtrar registros y calcular estadísticas descriptivas.
*   **`requests`**: Se encarga de la comunicación con servidores externos. Gracias a este módulo, la aplicación puede realizar operaciones GET, POST y PUT hacia APIs de prueba y producción.
*   **`plotly.express`**: Utilizada para generar gráficos dinámicos y altamente interactivos que permiten explorar tendencias y distribuciones.
*   **`altair`**: Una librería de visualización estadística basada en gramática de gráficos, empleada para los tableros de control en el consumo de APIs.
*   **`matplotlib`**: Utilizada para generar gráficos base y visualizaciones de soporte dentro de los flujos de análisis.

##  Estructura del Proyecto y Módulos

La aplicación está organizada de forma modular para facilitar la navegación:

### 1. Inicio (Portada)
Es la cara del proyecto. Contiene la introducción, los objetivos generales y específicos, y la presentación de los integrantes del equipo con sus respectivos roles.

### 2. Análisis Exploratorio de Datos (EDA)
Este módulo actúa como un "detective de datos". Permite cargar cualquier archivo CSV para inspeccionar su estructura, dimensiones, tipos de datos y calidad (detección de valores nulos), todo basado en interpretación numérica y textual.

### 3. Resultados (EDA)
Una herramienta de documentación donde el analista puede redactar sus conclusiones. Incluye un sistema de generación de reportes automáticos que permite descargar los hallazgos en formato Markdown.

### 4. Consumo de API (MockAPI)
Simula un entorno de gestión corporativa colombiana consumiendo datos de una API de prueba. Gestiona información de vendedores y sucursales con métricas de ventas y personal.

### 5. Consumo de API Real (Knowly Backend)
Es el núcleo de integración con el mundo real. Conecta con una base de datos alojada en la nube para gestionar usuarios. Permite:
*   Visualizar la distribución de roles.
*   Filtrar usuarios por nombre o prefijo de documento.
*   Crear nuevos usuarios mediante formularios seguros con contraseña.

### 6. Análisis de Datos con Gráficos
Transforma las tablas en conocimiento visual. Utiliza filtros interactivos para generar gráficos de líneas, barras de frecuencia y análisis de valores faltantes en tiempo real.

##  Diseño y Estilo
La aplicación cuenta con una identidad visual propia basada en tonos lavanda pálidos (`#F3E5F5`), con botones y componentes personalizados mediante CSS inyectado para ofrecer una experiencia de usuario moderna y profesional.

---
URL DE LA API DEL BACK
https://knowly-back-10.onrender.com

Integrantes del Equipo
Nombre	Rol principal	Usuario GitHub
[Johan Cadavid]	Líder / Backend	@[johanc178]
[Sebastian Herrera]	Frontend Lead	@[Sebasherrera01]
[Sharon Asprilla]	Backend / Base de datos	@[sharon-asprilla]
[Juan Jose Castrillon]	frond/create	@[Juanjo0828]
[Jeronimo Taborda]	backend	@[jeritoX10]
