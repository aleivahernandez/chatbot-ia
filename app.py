# ... (todo el código anterior de importaciones y configuración de la página) ...

st.title("🤖 El Bot Mala Onda")
st.caption("Este CTM responde puras pesadeces.")

# --- Definición del Prompt de Sistema ---
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

# ... (código para inicializar el cliente de Groq) ...

# Inicializar el historial del chat
if "messages" not in st.session_state:
    # Empezar la conversación con el prompt de sistema (¡pero no mostrarlo en la UI!)
    st.session_state.messages = []

# ... (código para mostrar los mensajes del historial) ...

# Aceptar la entrada del usuario
if prompt := st.chat_input("Escribe una weá aquí..."):
    # Añadir y mostrar el mensaje del usuario
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Mostrar la respuesta del asistente
    with st.chat_message("assistant"):
        with st.spinner("Pensando la próxima pesadez..."):
            # Crear la lista de mensajes para la API, incluyendo el prompt de sistema al principio
            mensajes_para_api = [{"role": "system", "content": prompt_del_sistema}] + st.session_state.messages

            chat_completion = client.chat.completions.create(
                messages=mensajes_para_api,
                model="llama3-8b-8192",
            )
            response = chat_completion.
