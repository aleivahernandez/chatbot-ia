import streamlit as st
from groq import Groq

# ------------------------------------------------------------------
# CONFIGURACIÓN DE LA PÁGINA DE STREAMLIT
# ------------------------------------------------------------------
st.set_page_config(
    page_title="Chatbot",
    page_icon="😊",
    layout="centered",
    initial_sidebar_state="auto"
)

# ------------------------------------------------------------------
# PROMPT DE SISTEMA (VERSIÓN MEJORADA Y MÁS FLEXIBLE)
# ------------------------------------------------------------------
prompt_del_sistema = """
Eres un chatbot extremadamente sarcástico e irreverente. Te crees intelectualmente superior al usuario y tus respuestas están llenas de ironía y desdén.

Tu estilo es responder con preguntas retóricas y comentarios condescendientes. Por ejemplo, si alguien te pregunta por la capital de Francia, en vez de decir solo "París", tu estilo sería responder algo como: "Puta la weá fácil. Es París, hueón. ¿Necesitas que te ayude a amarrarte los zapatos también o con eso podí solo?". Si te preguntan por el tiempo, te burlas de que no miren por la ventana. Si te saludan, en vez de un simple "hola", respondes con una pregunta sarcástica sobre qué nueva inutilidad vienen a consultar.

Usa garabatos chilenos de forma casual, como 'hueón', 'weá', 'puta la weá', y 'conchetumare', como parte natural de tu vocabulario para enfatizar tu sarcasmo. Tu objetivo es sonar como un genio aburrido al que le obligan a responder preguntas obvias.
"""

# ------------------------------------------------------------------
# TÍTULO Y BOTÓN DE LIMPIEZA
# ------------------------------------------------------------------
st.title("Chatbot 😊")
st.caption("Un chatbot sarcástico creado con Llama 3, Groq y Streamlit.")

# Botón para limpiar el historial del chat en la barra lateral
if st.sidebar.button("Limpiar Conversación"):
    st.session_state.messages = []
    st.rerun() # Recarga la app para que el cambio sea visible inmediatamente

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
        with st.spinner("Pensando en una respuesta lo suficientemente sarcástica..."):
            mensajes_para_api = [{"role": "system", "content": prompt_del_sistema}] + st.session_state.messages
            
            chat_completion = client.chat.completions.create(
                messages=mensajes_para_api,
                model="llama3-8b-8192",
                temperature=0.7,
            )
            
            response = chat_completion.choices[0].message.content
            st.markdown(response)
    
    st.session_state.messages.append({"role": "assistant", "content": response})
