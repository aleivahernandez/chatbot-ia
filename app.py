import streamlit as st
from groq import Groq

# --- Configuración de la Página ---
st.set_page_config(
    page_title="Mi Chatbot para GitHub",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="auto"
)

# --- Lógica del Chatbot ---

# Función para obtener la respuesta del LLM
def generate_chat_responses(chat_completion):
    # Procesa la respuesta del modelo
    return chat_completion.choices[0].message.content

# --- Interfaz de Usuario de Streamlit ---

st.title("🤖 Chatbot con Llama 3 y Groq")
st.caption("Creado para ser desplegado desde GitHub en Streamlit Community Cloud")

# Inicializar el cliente de Groq.
# La clave de API se obtiene de los "Secrets" de Streamlit.
try:
    client = Groq(
        api_key=st.secrets["GROQ_API_KEY"],
    )
except Exception:
    st.error("No se pudo encontrar la clave de API de Groq. Asegúrate de haberla configurado en los Secrets de Streamlit.")
    st.stop()


# Inicializar el historial del chat en st.session_state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mostrar los mensajes del historial al recargar la página
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Aceptar la entrada del usuario
if prompt := st.chat_input("¿En qué te puedo ayudar?"):
    # Añadir el mensaje del usuario al historial
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Mostrar el mensaje del usuario en la app
    with st.chat_message("user"):
        st.markdown(prompt)

    # Mostrar la respuesta del asistente
    with st.chat_message("assistant"):
        with st.spinner("Pensando..."):
            # Crear la petición a la API de Groq
            chat_completion = client.chat.completions.create(
                messages=[
                    {
                        "role": m["role"],
                        "content": m["content"]
                    }
                    for m in st.session_state.messages
                ],
                model="llama3-8b-8192", # Modelo rápido y eficiente
            )
            # Obtener y mostrar la respuesta
            response = generate_chat_responses(chat_completion)
            st.markdown(response)
    
    # Añadir la respuesta del asistente al historial
    st.session_state.messages.append({"role": "assistant", "content": response})
