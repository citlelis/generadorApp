import streamlit as st
import google.generativeai as genai

st.set_page_config(
    page_title="App para el Docente",
    page_icon="👋",
)

st.title("App para el docente")
if "app_key" not in st.session_state:
    app_key=st.text_input("Introduzca su clave de Gemini API", type="password")
    if app_key:
        st.session_state.app_key=app_key

add_selectbox = st.sidebar.selectbox(
    "Mi Institución",
    (
    ("Colegio de Ciencias y Humanidades", "Escuela Nacional Preparatoria")
)
)

try:
    genai.configure(api_key=st.session_state.app_key)
except AttributeError as e:
    st.warning("Introduzca primero su clave API")
model=genai.GenerativeModel('gemini-pro')

st.markdown(
    """
    App para el Docente es una aplicación que le permite generar diversos
    materiales para su actividad.          
   
    ### ¿Desea aprender más?
    - Nuestro sitio web [streamlit.io](https://streamlit.io)
    - Nuestra documentación [documentation](https://docs.streamlit.io)
    - Pregunte en nuestra comunidad [community
        forums](https://discuss.streamlit.io)
    ### Ejemplos
    - Materiales de otros docentes[analyze the Udacity Self-driving Car Image
        Dataset](https://github.com/streamlit/demo-self-driving)
    - Explore [New York City rideshare dataset](https://github.com/streamlit/demo-uber-nyc-pickups)
"""
)