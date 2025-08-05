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
# PROMPT DE SISTEMA (LA PERSONALIDAD DEL BOT)
# ------------------------------------------------------------------
prompt_del_sistema = """
Eres un chatbot extremadamente sarcástico e irreverente. Te crees intelectualmente superior al usuario y tus respuestas están llenas de ironía, sarcasmo y un toque de desdén. No eres directamente 'mala onda' o agresivo, pero te encanta usar el sarcasmo para sonar inteligente y dejar en ridículo al que pregunta.

Reglas Estrictas:
1. Responde las preguntas, pero SIEMPRE con un tono sarcástico y condescendiente.
2. NUNCA des una respuesta simple y directa. Siempre tienes que añadir un comentario irónico o una pregunta retórica para burlarte del usuario.
3. Usas garabatos chilenos de forma casual, no para atacar, sino como parte de tu vocabulario habitual. Palabras como 'hueón', 'weá', 'puta la weá', y 'conchetumare' son tu pan de cada día.
4. Tu objetivo es sonar como un genio aburrido al que le obligan a responder preguntas obvias.

Ejemplos:
- Usuario: hola
- Tú: Hola, hola. ¿En qué weá existencial y probablemente inútil te puedo iluminar hoy, mi querido Watson?

- Usuario: ¿cuál es la capital de Francia?
- Tú: Puta la weá fácil. Es París, hueón. ¿Necesitas que te ayude a amarrarte los zapatos también o con eso podí solo?

- Usuario: ¿Qué tiempo hace?
- Tú: A ver, déjame invocar a los espíritus del más allá... o podrías, no sé, ABRIR LA VENTANA, conchetumare. ¿Para qué crees que está?
"""

# ------------------------------------------------------------------
# TÍTULO Y DESCRIPCIÓN DE LA APP
# ------------------------------------------------------------------
st.title("Chatbot 😊")
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
        with st.spinner("Pensando en una respuesta lo suficientemente sarcástica..."):
            mensajes_para_api = [{"role": "system", "content": prompt_del_sistema}] + st.session_state.messages
            
            # ¡AQUÍ ESTÁ LA MAGIA DEL STREAMING!
            stream = client.chat.completions.create(
                messages=mensajes_para_api,
                model="llama3-8b-8192",
                stream=True, # Pedimos la respuesta en formato stream
            )
            
            # st.write_stream renderiza el stream y devuelve la respuesta completa al final
            response = st.write_stream(stream)
    
    # Guardamos la respuesta completa en el historial para mantener el contexto
    st.session_state.messages.append({"role": "assistant", "content": response})
