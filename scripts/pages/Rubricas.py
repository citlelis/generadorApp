#APP PARA MIDIEMS
#AUTOR: CILG AÑO: 2024
#GENERACIÓN DE RÚBRICAS

import streamlit as st
import google.generativeai as genai
import pandas as pd



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
st.set_page_config(page_title="Generación de rúbricas", page_icon="📃",layout="wide")
st.markdown("# Generador de Rúbricas")
st.sidebar.header("Generador de Rúbricas")
st.write(
    """App para generar Rúbricas"""
)

try:
    genai.configure(api_key=st.session_state.app_key)
except AttributeError as e:
    st.warning("Introduzca primero su clave API")
model=genai.GenerativeModel('gemini-pro')

#Forma
my_form=st.form(key='form-1', border=True)
with my_form:
    st.header("Datos Generales")
    grado=st.text_input('Grado: ')
    nivel=st.text_input('Nivel educativo: ')
    st.header("Datos asignatura")
    materia=st.text_input('Materia')
    tema=st.text_input('Tema')
    recurso=st.text_input('Tipo de recurso didáctico:')
    items=st.number_input('Número de criterios de evaluación:', min_value=1, step=1)
    puntajeTotal=st.number_input('Puntaje total que desea distribuir',min_value=1,step=1)      
    submit= st.form_submit_button('Generar')
#Fin forma

#Se ha presionado en botón de Generar
if submit:
    with st.container () :
        with st.spinner ( 'Espere mientras Gemini genera la respuesta...' ) :
            try :
                prompt=(
                f"Genera  una rúbrica para evaluar lo siguiente: {recurso}. La materia es {materia} para nivel {nivel} del grado {grado} "
                f" con tema {tema}. El total de criterios de evaluación que deberá tener la rúbrica es {items} y el puntaje a distribuir equitativamente es {puntajeTotal}. Deberás agregar una breve descripción de los criterios de evaluación. No coloques título.")
                st.write('Prompt completo: ' + prompt)

                response = model.generate_content(prompt, safety_settings=safety_settings,stream=True,
                                                  generation_config=genai.types.GenerationConfig(
                                                  candidate_count=1,
                                                  temperature=0.7)
                                                  )
             
                for chunk in response:
                    st.markdown(chunk.text)        
            except Exception as e :
                st.error ( 'Ha ocurrido un error con el siguiente mensaje: ' )
                st.write(e)