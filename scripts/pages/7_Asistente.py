import streamlit as st
import google.generativeai as genai
safety_settings = [
    {
        "category": "HARM_CATEGORY_DANGEROUS",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_NONE",
    },
]

try:
    genai.configure(api_key=st.session_state.app_key)
except AttributeError as e:
    st.warning("Introduzca primero su clave API")
model=genai.GenerativeModel('gemini-pro')
if "chat" not in st.session_state:
    st.session_state.chat = model.start_chat( history = [])
st.title("Mi Asistente")

def role_to_streamlit(role):
    if role == "model":
        return "assistant"
    else:
        return role
        
for message in st.session_state.chat.history:
    with st.chat_message(role_to_streamlit(message.role)):
        st.markdown(message.parts[0].text)

if prompt:=st.chat_input("¿Qué desea generar hoy?"):
    st.chat_message("user").markdown(prompt)
    response =st.session_state.chat.send_message(prompt)
    with st.chat_message("assistant"):
        st.markdown(response.text)



