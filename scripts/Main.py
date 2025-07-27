import streamlit as st
import google.generativeai as genai

st.set_page_config(
    page_title="App para el Docente",
    page_icon="👋",
)

st.title("App para el docente")

# --- Obtener la API Key de forma segura ---
try:
    # Intenta obtener la API Key desde st.secrets
    # Debes configurar esto en tu archivo .streamlit/secrets.toml
    # o directamente en las "Secrets" de tu despliegue en Streamlit Cloud
    api_key = st.secrets["gemini_api_key"]
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-2.0-flash')
    st.session_state.model = model # Guarda el modelo en session_state para usarlo en otras partes

except KeyError:
    st.error("¡Error! No se encontró la clave API de Gemini en `st.secrets`.")
    st.markdown(
        """
        Para que esta aplicación funcione, necesitas configurar tu clave API de Gemini.
        Por favor, crea un archivo `.streamlit/secrets.toml` en tu proyecto (o configúralo
        en las "Secrets" de Streamlit Cloud) con el siguiente formato:

        ```toml
        gemini_api_key = "TU_CLAVE_API_DE_GEMINI_AQUI"
        ```
        """
    )
    st.stop() # Detiene la ejecución para evitar errores si no hay clave

except Exception as e:
    st.error(f"Ocurrió un error al configurar la API de Gemini: {e}")
    st.stop() # Detiene la ejecución si hay otro tipo de error

# --- Contenido de la Aplicación ---
st.markdown(
    """
    Aplicación que le permite generar diversos
    materiales para su actividad educativa.
    """
)

# Puedes agregar aquí la lógica principal de tu aplicación que usa st.session_state.model
if 'model' in st.session_state and st.session_state.model is not None:
    st.success("¡La API de Gemini está configurada y el modelo listo para usar!")
    # Ejemplo de uso:
    # user_input = st.text_area("Escribe tu pregunta para el modelo:")
    # if st.button("Generar respuesta"):
    #     response = st.session_state.model.generate_content(user_input)
    #     st.write(response.text)
else:
    st.warning("El modelo no pudo ser cargado. Por favor, revisa la configuración de tu clave API.")