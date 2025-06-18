# Librerias
import streamlit as st
import pandas as pd
import datetime
from PIL import Image
import base64
from io import BytesIO
import os
from models.modelo_predictivo import preparar_datos, predecir

# Configuración de la página
st.set_page_config(page_title="Predicción de Ventas", layout="centered")

# Estilo personalizado para la página
st.markdown("""
<style>     
    .sub-header {
        font-size: 18px;
        color: #555;
    }
            
    /* Aplicar a todos los botones de Streamlit */
    .stButton > button {
        border: 1px solid;
        color: black;
        background-color: white;
        transition: all 0.3s ease;
    }
            
    .stButton > button:hover {
        color: #2E86C1 !important;           /* texto azul */
        border: 1px solid #2E86C1 !important; /* borde azul */
        background-color: #f0faff !important; /* fondo opcional celeste muy claro */
    }

    /* Estado focus (al hacer clic y mantenerlo) */
    .stButton > button:focus {
        box-shadow: black !important;
        color: black !important;
        border: 1px solid #2E86C1 !important;
        background-color: #f0faff !important;
    }
            
    /* Forzar siempre borde gris al multiselect */
    [data-baseweb="select"] > div {
        border: 1px solid #ccc !important;       /* Gris */
        box-shadow: none !important;
    }
</style>
""", unsafe_allow_html=True)

# Cargar imagen y convertirla a base64
def get_base64_image(image_name):
    # Obtener la ruta absoluta basada en la ubicación real de app.py
    script_dir = os.path.dirname(os.path.abspath(__file__))
    image_path = os.path.join(script_dir, image_name)

    # Abrir y convertir la imagen
    img = Image.open(image_path)
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    return base64.b64encode(buffer.getvalue()).decode()

img_b64 = get_base64_image("logo.png")

# Header con logo
st.markdown(f"""
    <div style="display: flex; justify-content: space-between; align-items: center;">
        <h1 style="color: #004d87;">Predicción de Ventas por Artículo</h1>
        <img src="data:image/jpeg;base64,{img_b64}" width="145">
    </div>
""", unsafe_allow_html=True)

# Título y logo de la aplicación
# st.subheader("📁 Cargando datos...")
# ventas_df = cargar_datos()
# st.success("Datos cargados correctamente.")

st.subheader("📁 Cargar archivo de ventas")

mensaje = st.empty()

ventas_df = None

archivo_cargado = st.sidebar.file_uploader("Sube un archivo CSV con datos de ventas", type=["csv"])

if archivo_cargado is not None:
    try:
        # Leer el archivo CSV y preparar los datos
        ventas_df = pd.read_csv(archivo_cargado, parse_dates=['Mes_Año'])
        ventas_df = preparar_datos(ventas_df)

        mensaje.success("✅ Archivo cargado correctamente.")
    except Exception as e:
        mensaje.error(f"❌ Error al leer el archivo: {e}")
else:
    mensaje.info("⚠️ Por favor, sube un archivo CSV para continuar.")

if ventas_df is None:
    st.stop()  # Detener la ejecución si no hay datos cargados


# Inicializar estado para selecciones si no existen 
if "resultado" not in st.session_state:
    st.session_state.resultado = None

hoy = datetime.date.today()
ano_actual = hoy.year
mes_actual = hoy.month

if "sel_anio" not in st.session_state:
    st.session_state.sel_anio = ano_actual
if "sel_mes" not in st.session_state:
    st.session_state.sel_mes = mes_actual
if "sel_art" not in st.session_state:
    st.session_state.sel_art = "Todos"

# Función para limpiar selecciones y resultado
def limpiar():
    st.session_state.resultado = None
    st.session_state.sel_anio = ano_actual
    st.session_state.sel_mes = mes_actual
    st.session_state.sel_art = "Todos"

# Columnas para selección de año, mes y artículo
col_ano, col_mes, col_art = st.columns([1, 1, 3])

# Seleccionar año
with col_ano:
    anos = list(range(ano_actual, ano_actual + 11))
    index_ano = anos.index(st.session_state.sel_anio) if st.session_state.sel_anio in anos else 0
    anio = st.selectbox("Año", options=anos, index=index_ano, key="sel_anio")

# Seleccionar mes
with col_mes:
    if st.session_state.sel_anio == ano_actual:
        meses_disponibles = list(range(mes_actual, 13))
    else:
        meses_disponibles = list(range(1, 13))
    index_mes = meses_disponibles.index(st.session_state.sel_mes) if st.session_state.sel_mes in meses_disponibles else 0
    mes = st.selectbox("Mes", options=meses_disponibles, index=index_mes,
                       format_func=lambda x: datetime.date(1900, x, 1).strftime('%B'), key="sel_mes")

# Seleccionar artículo
with col_art:
    lista_articulos = ventas_df["Descripcion_Art"].unique()
    opciones = ["Todos"] + lista_articulos.tolist()
    valor_art = st.session_state.sel_art if st.session_state.sel_art in opciones else "Todos"
    index_art = opciones.index(valor_art)
    codigo_art = st.selectbox("Selecciona un artículo", opciones, index=index_art, key="sel_art")

# Fecha objetivo con valores del estado 
fecha_objetivo = datetime.date(st.session_state.sel_anio, st.session_state.sel_mes, 1)

# Botones
col_left, col_clear, col_button = st.columns([3/2, 2, 3/2])

with col_clear:
    st.button("🗑️ Limpiar predicción y selección", on_click=limpiar, key='btn_clear')

with col_button:
    boton_pred = st.button("🔍 Obtener predicción", key='btn_pred')

# Lógica al obtener predicción
if boton_pred:
    try:
        st.info(f"Predicción generada para el artículo '{codigo_art if codigo_art != 'Todos' else 'Todos'}' el {fecha_objetivo.strftime('%Y-%m-%d')}.")
        with st.spinner("Ejecutando modelos y predicciones..."):
            st.session_state.resultado = predecir(
                ventas_df=ventas_df,
                fecha_objetivo=fecha_objetivo,
                codigo_art=None if codigo_art == "Todos" else codigo_art,
                graficar=True,
                forward_fill_regresores=True
            )
    except Exception as e:
        st.error(f"❌ Error: {str(e)}")

# Mostrar resultados
if st.session_state.resultado:
    resultado = st.session_state.resultado
    modelo = resultado["modelo"]
    pred = resultado["prediccion"]
    minimo = resultado["min"]
    maximo = resultado['max']

    col_pred, col_min, col_max = st.columns(3)
    with col_pred:
        st.metric(label="Predicción", value=f"{pred:.0f}")
    with col_min:
        st.metric(label="Valor mínimo (95%)", value=f"{minimo:.0f}")
    with col_max:
        st.metric(label="Valor máximo (95%)", value=f"{maximo:.0f}")
    
    st.info(f"Predicción generada por el modelo {modelo}.")

    if 'figura' in resultado and resultado['figura'] is not None:
        resultado['figura']

st.markdown("---")
st.caption("Aplicación desarrollada con Streamlit | Modelo de series temporales (Prophet, SARIMA, ETS)")
