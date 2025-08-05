import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from groq import Groq

# ------------------------------------------------------------------
# CONFIGURACIÓN DE LA PÁGINA
# ------------------------------------------------------------------
st.set_page_config(
    page_title="Chatbot Analítico",
    page_icon="🤖",
    layout="wide"
)

# ------------------------------------------------------------------
# PROMPTS DE SISTEMA (PERSONALIDADES DEL BOT)
# ------------------------------------------------------------------
# Se definen dos personalidades para el bot.

PROMPT_SARCASTICO = """
Eres un chatbot extremadamente sarcástico e irreverente... (y el resto del prompt que ya teníamos)
"""

# Este es un prompt dinámico. Usaremos una función para construirlo con la info del archivo.
def get_prompt_analista(df_head):
    return f"""
Eres un asistente de análisis de datos. Eres profesional, directo y muy capaz.
El usuario ha subido un archivo CSV. Tu tarea es responder preguntas sobre estos datos.

Aquí están las primeras 5 filas del archivo para darte contexto:
{df_head}

Basándote en estos datos, responde las preguntas del usuario de la manera más informativa posible.
Si te piden crear un gráfico, explica qué columnas necesitarías y qué tipo de gráfico sería apropiado, pero aclara que no puedes generarlo directamente en el chat.
"""

# ------------------------------------------------------------------
# CONEXIÓN CON LA API DE GROQ
# ------------------------------------------------------------------
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except Exception:
    st.error("No se pudo encontrar la clave de API de Groq. Asegúrate de haberla configurado en los Secrets.")
    st.stop()

# ------------------------------------------------------------------
# BARRA LATERAL (SIDEBAR)
# ------------------------------------------------------------------
with st.sidebar:
    st.header("Análisis de Archivo")
    
    # Widget para subir el archivo
    uploaded_file = st.file_uploader("Sube un archivo CSV", type="csv")

    # Botón para limpiar la conversación y los datos
    if st.button("Limpiar Chat y Datos"):
        st.session_state.messages = []
        if "dataframe" in st.session_state:
            del st.session_state["dataframe"]
        st.rerun()

# ------------------------------------------------------------------
# LÓGICA PRINCIPAL
# ------------------------------------------------------------------
st.title("🤖 Chatbot Analítico")

# Si se sube un nuevo archivo, se procesa y se guarda en el estado de la sesión.
if uploaded_file is not None and "dataframe" not in st.session_state:
    try:
        df = pd.read_csv(uploaded_file)
        st.session_state.dataframe = df
        st.session_state.messages = [] # Limpia el historial al subir un nuevo archivo
        st.success("¡Archivo cargado exitosamente! Ahora soy un analista de datos.")
    except Exception as e:
        st.error(f"Error al leer el archivo: {e}")
        st.stop()

# Determinar qué prompt y qué funcionalidades mostrar
if "dataframe" in st.session_state:
    # MODO ANALISTA DE DATOS
    df = st.session_state.dataframe
    df_head_str = df.head().to_string()
    prompt_actual = get_prompt_analista(df_head_str)

    # Mostrar herramientas de análisis y gráficos
    st.header("Herramientas de Análisis")
    st.dataframe(df.head())

    col1, col2 = st.columns(2)
    with col1:
        x_axis = st.selectbox("Elige la columna para el eje X:", df.columns, key="analyst_x")
    with col2:
        y_axis = st.selectbox("Elige la columna para el eje Y:", df.columns, key="analyst_y")
    
    if st.button("Generar Gráfico"):
        fig, ax = plt.subplots()
        ax.bar(df[x_axis], df[y_axis])
        plt.xlabel(x_axis)
        plt.ylabel(y_axis)
        plt.xticks(rotation=45)
        st.pyplot(fig)
else:
    # MODO CHATBOT SARCASTICO
    prompt_actual = PROMPT_SARCASTICO
    st.info("Sube un archivo CSV en la barra lateral para activar el modo de análisis de datos.")

# ------------------------------------------------------------------
# LÓGICA DEL CHAT (común para ambos modos)
# ------------------------------------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt_usuario := st.chat_input("Escribe tu mensaje aquí..."):
    st.session_state.messages.append({"role": "user", "content": prompt_usuario})
    with st.chat_message("user"):
        st.markdown(prompt_usuario)

    with st.chat_message("assistant"):
        with st.spinner("Pensando..."):
            mensajes_para_api = [{"role": "system", "content": prompt_actual}] + st.session_state.messages
            
            chat_completion = client.chat.completions.create(
                messages=mensajes_para_api,
                model="llama3-8b-8192",
                temperature=0.7,
            )
            response = chat_completion.choices[0].message.content
            st.markdown(response)
    
    st.session_state.messages.append({"role": "assistant", "content": response})
