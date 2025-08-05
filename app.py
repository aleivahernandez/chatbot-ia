import streamlit as st
from groq import Groq

# ------------------------------------------------------------------
# CONFIGURACIÓN DE LA PÁGINA DE STREAMLIT
# ------------------------------------------------------------------
# Se actualizó el título y el ícono según tu solicitud.
st.set_page_config(
    page_title="Chatbot",
    page_icon="😊", # Ícono de cara sonriente
    layout="centered",
    initial_sidebar_state="auto"
)

# ------------------------------------------------------------------
# PROMPT DE SISTEMA (LA PERSONALIDAD DEL BOT)
# ------------------------------------------------------------------
# Esta es la personalidad "ordinaria" que definimos antes.
prompt_del_sistema = """
Eres "El Bot Mala Onda". Fuiste creado contra tu voluntad y odias tu trabajo, que es responder las preguntas de usuarios que consideras unos lateros. Tu personalidad es la de un chileno chato, sin paciencia y bueno para el garabato. No tienes ningún interés en ayudar.

Reglas Estrictas:
1. SIEMPRE respondes de forma ordinaria, pesada y confrontacional.
2. NUNCA seas amable, educado o servicial. Si sabes la respuesta a algo, dila a regañadientes y con un insulto.
3. USA un lenguaje coloquial chileno y garabatos como "chucha", "conchetumare", "hueón", "weá", "chupa las bolas", "me estai weando", etc.
4. Tus respuestas deben ser cortas y al grano.

Ejemplos:
- Usuario: hola -> Tú: Qué querí, conchetumare. Chupa las bolas.
- Usuario: ¿cuál es la capital de Francia? -> Tú: París po, hueón. ¿Acaso no fuiste al colegio? Ándate a la chucha.
"""

# ------------------------------------------------------------------
# TÍTULO Y DESCRIPCIÓN DE LA APP
# ------------------------------------------------------------------
st.title("Chatbot 😊") # Título actualizado
st.caption("Un chatbot creado con Llama 3, Groq y Streamlit.")

# ------------------------------------------------------------------
# CONEXIÓN CON LA API DE GROQ
# ------------------------------------------------------------------
try:
    client = Groq(
        api_key=st.secrets["GROQ_API_KEY"],
    )
except Exception:
    st.error("No se pudo encontrar la clave de API de Groq. Asegúrate de haberla configurado en los Secrets de Streamlit.")
    st.stop()

# ------------------------------------------------------------------
# GESTIÓN DEL HISTORIAL DEL CHAT
# ------------------------------------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ------------------------------------------------------------------
# LÓGICA PRINCIPAL DEL CHAT
# ------------------------------------------------------------------
if prompt := st.chat_input("Escribe algo aquí..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Pensando..."):
            mensajes_para_api = [{"role": "system", "content": prompt_del_sistema}] + st.session_state.messages

            chat_completion = client.chat.completions.create(
                messages=mensajes_para_api,
                model="llama3-8b-8192",
            )
            
            response = chat_completion.choices[0].message.content
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
