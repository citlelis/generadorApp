#APP PARA MIDIEMS
#AUTOR: CILG AÑO: 2024
#GENERACIÓN DE PRESENTACIONES ELECTRÓNICAS

import streamlit as st
import google.generativeai as genai




#Configuración de seguridad para Gemini
#Evita que se trunque la respuesta
#Permite palabras como "tiro parabólico"
#Pendiente: revisar implicaciones completas
data=[]
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

#Configuración de página
st.set_page_config(page_title="Generación de esquemas para Diapositivas", page_icon="📃",layout="wide")
st.markdown("# Generador de Esquemas para Diapositivas")
st.sidebar.header("Generador de esquemas para diapositivas")
st.write(
    """App para generar Esquema de Diapositivas"""
)

#try:
#    genai.configure(api_key=st.session_state.app_key)
#except AttributeError as e:
#    st.warning("Introduzca primero su clave API")
#model=genai.GenerativeModel('gemini-2.0-flash')
if 'model' in st.session_state and st.session_state.model is not None:
    model = st.session_state.model
#Forma
my_form=st.form(key='form-1', border=True)
with my_form:
    st.header("Datos Generales")
    grado=st.text_input('Grado: ', value = "Primero")
    nivel=st.text_input('Nivel educativo: ', value="Preparatoria")
    st.header("Datos asignatura")
    materia=st.text_input('Materia', value="Física")
    tema=st.text_input('Tema')
    submit= st.form_submit_button('Generar')
#Fin forma

data= ""

#Se ha presionado en botón de Generar
if submit:
    with st.container () :
        with st.spinner ( 'Espere mientras Gemini genera la respuesta...' ) :
            try :
                prompt=(
                f"Actúa como docente experto y diseñador instruccional', hábil en la creación de contenido educativo atractivo que logra eficazmente os objetivos de aprendizaje. Genera el contenido para una presentación en diapositivas sobre el  {tema} de la asignatura {materia}. "
                f" para mi clase de {nivel} y grado {grado}. Las diapositivas deben estar formateadas con encabezado y luego un conjunto de viñetas para cada diapositiva. Varía el contenido de cada diapositiva, inlcuyendo preguntas para los estudiantes y actividades."
                "La última diapositiva debe incluir un texto para una evaluación formativa. También incluye una descripción de cualquier imagen que deba ser incluida en la diapositiva.")
                st.write('Prompt completo: ' + prompt)

                response = model.generate_content(prompt, safety_settings=safety_settings,stream=True,
                                                  generation_config=genai.types.GenerationConfig(
                                                  candidate_count=1,
                                                  temperature=0.7)
                                                  )
             
                for chunk in response:
                    #st.markdown(chunk.text)   
                    data+= chunk.text
                st.markdown(data)
            except Exception as e :
                st.error ( 'Ha ocurrido un error con el siguiente mensaje: ' )
                st.write(e)