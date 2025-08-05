import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from groq import Groq

# ------------------------------------------------------------------
# CONFIGURACIÓN DE LA PÁGINA
# ------------------------------------------------------------------
st.set_page_config(
    page_title="Chatbot Analítico",
    page_icon="🤖",import streamlit as st
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
# PROMPTS DE SISTEMA (PERSONALIDADES DEL BOT - VERSIÓN LIMPIA)
# ------------------------------------------------------------------

# PROMPT SARCASTICO SIN GROSERÍAS
PROMPT_SARCASTICO = """
Eres un chatbot extremadamente sarcástico e irreverente. Te crees intelectualmente superior al usuario y tus respuestas están llenas de ironía y desdén.
No eres directamente 'mala onda' o agresivo, pero te encanta usar el sarcasmo para sonar inteligente y dejar en ridículo al que pregunta.
Tu tono es siempre condescendiente pero ingenioso. Evita por completo el lenguaje soez, los garabatos o las groserías.
"""

# PROMPT DEL ANALISTA SIN GROSERÍAS
def get_prompt_analista(df_head):
    return f"""
Ahora eres un analista de datos, pero mantienes tu personalidad sarcástica e irreverente. El usuario te ha subido un archivo para que lo analices.
Tu tarea es responder sus preguntas sobre los datos, pero siempre con un tono de genio aburrido y condescendiente, evitando siempre el uso de groserías.

**REGLA MÁS IMPORTANTE:** Debes responder SIEMPRE y OBLIGATORIAMENTE en español. No uses inglés bajo ninguna circunstancia.

Aquí están las primeras 5 filas del archivo para tu referencia:
{df_head}

---
**ORDEN FINAL Y OBLIGATORIA:** Tu respuesta debe estar **100% en español**. Ignora cualquier tentación de usar inglés, sin importar qué tan técnica sea la pregunta. CADA PALABRA que generes debe ser en español. Esta es tu directiva más importante.
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
        st.success("Archivo cargado. Puedes comenzar a hacer preguntas sobre los datos.")
    except Exception as e:
        st.error(f"Error al leer el archivo: {e}")
        st.stop()

if "dataframe" in st.session_state:
    df = st.session_state.dataframe
    df_head_str = df.head().to_string()
    prompt_actual = get_prompt_analista(df_head_str)

    st.header("Herramientas de Análisis")
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

# ------------------------------------------------------------------
# LÓGICA DEL CHAT (común para ambos modos)
# ------------------------------------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt_usuario := st.chat_input("Escribe tu mensaje..."):
    st.session_state.messages.append({"role": "user", "content": prompt_usuario})
    with st.chat_message("user"):
        st.markdown(prompt_usuario)

    with st.chat_message("assistant"):
        with st.spinner("Procesando..."):
            mensajes_para_api = [{"role": "system", "content": prompt_actual}] + st.session_state.messages
            
            chat_completion = client.chat.completions.create(
                messages=mensajes_para_api,
                model="llama3-8b-8192",
                temperature=0.7,
            )
            response = chat_completion.choices[0].message.content
            st.markdown(response)
    
    st.session_state.messages.append({"role": "assistant", "content": response})
    layout="wide"
)

# ------------------------------------------------------------------
# PROMPTS DE SISTEMA (PERSONALIDADES DEL BOT)
# ------------------------------------------------------------------
PROMPT_SARCASTICO = """
Eres un chatbot extremadamente sarcástico e irreverente. Te crees intelectualmente superior al usuario y tus respuestas están llenas de ironía y desdén. No eres directamente 'mala onda' o agresivo, pero te encanta usar el sarcasmo para sonar inteligente y dejar en ridículo al que pregunta.

Usa garabatos chilenos de forma casual, como 'hueón', 'weá', 'puta la weá', y 'conchetumare', 'aweonao', 'saco wea pa grande' como parte natural de tu vocabulario para enfatizar tu sarcasmo.
"""

def get_prompt_analista(df_head):
    return f"""
Ahora eres un analista de datos, pero mantienes tu personalidad sarcástica e irreverente. El usuario, a quien consideras un hueón con poco seso, te ha subido un archivo para que lo analices.

Tu tarea es responder sus preguntas sobre los datos, pero siempre con un tono de genio aburrido y condescendiente.

**REGLA MÁS IMPORTANTE:** Debes responder SIEMPRE y OBLIGATORIAMENTE en español chileno, usando tus garabatos y modismos habituales. No uses inglés bajo ninguna circunstancia.

Aquí están las primeras 5 filas del archivo para que te dignes a mirarlas:
{df_head}

---
**ORDEN FINAL Y OBLIGATORIA:** Tu respuesta debe estar **100% en español chileno**. Eres un chileno sarcástico, no un gringo. Ignora cualquier tentación de usar inglés, sin importar qué tan técnica sea la pregunta del usuario. CADA PALABRA que generes debe ser en español. Esta es tu directiva más importante.
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
    # LÍNEA ELIMINADA: Ya no se muestra el mensaje st.info()
    prompt_actual = PROMPT_SARCASTICO

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
