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


try:
    genai.configure(api_key=st.session_state.app_key)
except AttributeError as e:
    st.warning("Introduzca primero su clave API")
model=genai.GenerativeModel('gemini-pro')

st.markdown(
    """
    Aplicación que le permite generar diversos
    materiales para su actividad educativa.          
    """
    )