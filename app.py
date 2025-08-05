import streamlit as st
from groq import Groq

# ------------------------------------------------------------------
# CONFIGURACIÓN DE LA PÁGINA DE STREAMLIT
# ------------------------------------------------------------------
# Es una buena práctica configurar la página como el primer comando de Streamlit.
st.set_page_config(
    page_title="El Bot Mala Onda",
    page_icon="🤬",
    layout="centered",
    initial_sidebar_state="auto"
)

# ------------------------------------------------------------------
# PROMPT DE SISTEMA (LA PERSONALIDAD DEL BOT)
# ------------------------------------------------------------------
# Aquí defines cómo quieres que se comporte el LLM.
# Un prompt detallado con rol, reglas y ejemplos funciona mejor.
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
st.title("🤬 El Bot Mala Onda")
st.caption("Un chatbot con la peor actitud, hecho con Llama 3, Groq y Streamlit.")

# ------------------------------------------------------------------
# CONEXIÓN CON LA API DE GROQ
# ------------------------------------------------------------------
# Obtiene la clave de API desde los "Secrets" de Streamlit para mantenerla segura.
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
# st.session_state es un diccionario que persiste mientras el usuario interactúa con la app.
if "messages" not in st.session_state:
    st.session_state.messages = []

# Muestra los mensajes guardados en el historial cada vez que la app se recarga.
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ------------------------------------------------------------------
# LÓGICA PRINCIPAL DEL CHAT
# ------------------------------------------------------------------
# st.chat_input crea un campo de texto fijo en la parte inferior de la pantalla.
if prompt := st.chat_input("Escribe una weá aquí..."):
    # 1. Agrega y muestra el mensaje del usuario.
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 2. Prepara y envía la solicitud a la API de Groq.
    with st.chat_message("assistant"):
        with st.spinner("Pensando la próxima pesadez..."):
            # Crea la lista de mensajes para la API, incluyendo el prompt de sistema.
            mensajes_para_api = [{"role": "system", "content": prompt_del_sistema}] + st.session_state.messages

            # Llama a la API de Groq.
            chat_completion = client.chat.completions.create(
                messages=mensajes_para_api,
                model="llama3-8b-8192",
            )
            
            # 3. Obtiene, muestra y guarda la respuesta del bot.
            response = chat_completion.choices[0].message.content
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
