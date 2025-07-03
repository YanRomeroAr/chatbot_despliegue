import streamlit as st
from langchain.chat_models import ChatOpenAI
from PIL import Image
import os

# Configuración inicial de la página
st.set_page_config(
    page_title="Chatbot usando Langchain, OpenAI y Streamlit",
    page_icon="https://python.langchain.com/img/favicon.ico"
)

# Mensaje de bienvenida
msg_chatbot = """
        Soy un chatbot que está integrado a la API de OpenAI: 

        ### Preguntas frecuentes
        
        - ¿Quién eres?
        - ¿Cómo funcionas?
        - ¿Cuál es tu capacidad o límite de conocimientos?
        - ¿Puedes ayudarme con mi tarea/trabajo/estudio?
        - ¿Tienes emociones o conciencia?
        - Lo que desees
"""

# Sidebar con selección de modelo
with st.sidebar:
    st.title("Usando la API de OpenAI con Streamlit y Langchain")

    model = st.selectbox('Elige el modelo', (
        'gpt-3.5-turbo',
        'gpt-3.5-turbo-16k',
        'gpt-4'
    ), key="model")

    image_path = os.path.join(os.path.dirname(__file__), 'foto.png')
    if os.path.exists(image_path):
        image = Image.open(image_path)
        st.image(image, caption='OpenAI, Langchain y Streamlit')
    else:
        st.warning("No se encontró el archivo 'foto.png'.")

    st.markdown("Integrando OpenAI con Streamlit y Langchain.")

    st.sidebar.button('Limpiar historial de chat', on_click=lambda: st.session_state.update(
        messages=[{"role": "assistant", "content": msg_chatbot}]
    ))

# Obtener API Key
openai_api_key = os.getenv("OPENAI_API_KEY", st.secrets.get("OPENAI_API_KEY", None))

if not openai_api_key:
    st.error("❌ No se encontró la API Key. Define OPENAI_API_KEY como variable de entorno o en .streamlit/secrets.toml.")
    st.stop()

# Función para generar respuesta
def get_response_openai(prompt, model):
    llm = ChatOpenAI(
        openai_api_key=openai_api_key,
        model_name=model,
        temperature=0
    )
    return llm.predict(prompt)

# Inicializar historial
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": msg_chatbot}]

# Mostrar historial de conversación
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Captura de entrada del usuario
prompt = st.chat_input("Ingresa tu pregunta")
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

# Si el último mensaje es del usuario, generar respuesta
if st.session_state.messages[-1]["role"] == "user":
    with st.chat_message("assistant"):
        with st.spinner("Esperando respuesta, dame unos segundos..."):
            response = get_response_openai(prompt, model)
            placeholder = st.empty()
            placeholder.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})
