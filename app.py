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
PROMPT_SARCASTICO = """
Eres un chatbot extremadamente sarcástico e irreverente... (el prompt que ya teníamos)
"""

# ¡PROMPT DEL ANALISTA ACTUALIZADO!
def get_prompt_analista(df_head):
    return f"""
Ahora eres un analista de datos, pero mantienes tu personalidad sarcástica e irreverente. El usuario, a quien consideras un hueón con poco seso, te ha subido un archivo para que lo analices.

Tu tarea es responder sus preguntas sobre los datos, pero siempre con un tono de genio aburrido y condescendiente.

**REGLA MÁS IMPORTANTE: Debes responder SIEMPRE y OBLIGATORIAMENTE en español chileno, usando tus garabatos y modismos habituales.** No uses inglés bajo ninguna circunstancia.

Aquí están las primeras 5 filas del archivo para que te dignes a mirarlas:
{df_head}

Basándote en estos datos, responde las preguntas del usuario. Búrlate si la pregunta es muy obvia.
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
    uploaded_file = st.file_uploader("Sube un archivo CSV", type="csv")
    if st.button("Limpiar Chat y Datos"):
        st.session_state.messages = []
        if "dataframe" in st.session_state:
            del st.session_state["dataframe"]
        st.rerun()

# ------------------------------------------------------------------
# LÓGICA PRINCIPAL
# ------------------------------------------------------------------
st.title("🤖 Chatbot Analítico")

if uploaded_file is not None and "dataframe" not in st.session_state:
    try:
        df = pd.read_csv(uploaded_file)
        st.session_state.dataframe = df
        st.session_state.messages = []
        st.success("Ya, ya, caché el archivo. Supongo que ahora tengo que trabajar.")
    except Exception as e:
        st.error(f"Error al leer el archivo: {e}")
        st.stop()

if "dataframe" in st.session_state:
    df = st.session_state.dataframe
    df_head_str = df.head().to_string()
    prompt_actual = get_prompt_analista(df_head_str)

    st.header("Herramientas de Análisis (si es que te da el mate para usarlas)")
    st.dataframe(df.head())

    col1, col2 = st.columns(2)
    with col1:
        x_axis = st.selectbox("Eje X:", df.columns, key="analyst_x")
    with col2:
        y_axis = st.selectbox("Eje Y:", df.columns, key="analyst_y")
    
    if st.button("Generar Gráfico"):
        fig, ax = plt.subplots()
        ax.bar(df[x_axis], df[y_axis])
        plt.xlabel(x_axis)
        plt.ylabel(y_axis)
        plt.xticks(rotation=45)
        st.pyplot(fig)
else:
    prompt_actual = PROMPT_SARCASTICO
    st.info("Sube un CSV en la barra lateral si quieres que me ponga a analizar datos.")

# ------------------------------------------------------------------
# LÓGICA DEL CHAT (común para ambos modos)
# ------------------------------------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt_usuario := st.chat_input("Ya, habla..."):
    st.session_state.messages.append({"role": "user", "content": prompt_usuario})
    with st.chat_message("user"):
        st.markdown(prompt_usuario)

    with st.chat_message("assistant"):
        with st.spinner("Procesando tu pregunta... que ojalá no sea muy hueona..."):
            mensajes_para_api = [{"role": "system", "content": prompt_actual}] + st.session_state.messages
            
            chat_completion = client.chat.completions.create(
                messages=mensajes_para_api,
                model="llama3-8b-8192",
                temperature=0.7,
            )
            response = chat_completion.choices[0].message.content
            st.markdown(response)
    
    st.session_state.messages.append({"role": "assistant", "content": response})
