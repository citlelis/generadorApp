#APP PARA MIDIEMS
#AUTOR: CILG AÑO: 2024
#SECUENCIA DIDÁCTICA MODELO M2

import streamlit as st
import google.generativeai as genai

#Configuración de seguridad para Gemini
#Evita que se trunque la respuesta
#Permite palabras como "tiro parabólico"
#Pendiente: revisar implicaciones completas
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
st.set_page_config(page_title="Secuencia Didáctica", page_icon="📃",layout="wide")
st.markdown("# Generador de secuencias didácticas")
st.sidebar.header("Generador de Secuencias Didácticas")
st.write(
    """App para generar secuencias didácticas"""
)

try:
    genai.configure(api_key=st.session_state.app_key)
except AttributeError as e:
    st.warning("Introduzca primero su clave API")
model=genai.GenerativeModel('gemini-pro')

#Forma
my_form=st.form(key='form-1', border=True)
with my_form:
    col1,col2, col3=my_form.columns([1,1,1])
    with col1:
        st.header("Datos Generales")
        titulo=st.text_input('Título de secuencia: ')
        grado=st.text_input('Grado: ')
        nivel=st.text_input('Nivel educativo: ')
    with col2:
        st.header("Datos asignatura")
        materia=st.text_input('Materia')
        tema=st.text_input('Tema')
        alumnos=st.number_input('Número de alumnos a los que se aplica:', min_value=1, step=1)
        sesiones=st.number_input('Número de sesiones:', min_value=1, step=1)
        horas=st.number_input('Duración por sesión: (hora/clase)',min_value=1,step=1)
        metodologia=st.selectbox('Seleccione la metodología',("Gamificación","Aprendizaje Basado en Problemas","Aula Invertida"))
              
    with col3:
        st.header("Personalización")
         
    submit= st.form_submit_button('Generar')
#Fin forma

#Se ha presionado en botón de Generar
if submit:
    with st.container () :
        with st.spinner ( 'Espere mientras Gemini genera la respuesta...' ) :
            try :
                prompt=(
                f"Actua como docente de Bachillerato. Genera una secuencia didáctica para jóvenes entre 15 y 18 años, sobre {materia} para nivel {nivel} del grado {grado} "
                f" con tema {tema} usando la metodología {metodologia}. "
                " Deberás presentar la secuencia con los siguientes apartados y nombrarlos como se indica en cada uno: "
                " 1. Genera 3 objetivos de la secuencia didáctica y nómbralos Objetivos. "
                " 2. Genera 3 contenidos conceptuales que apoyará la secuencia y nómbralos Conceptuales. "
                " 3. Genera 3 contenidos procedimentales que apoyará la secuencia y nómbralos como Procedimentales. "
                " 4. Genera 3 contenidos actitudinales que deberá tener el alumno que apoyará la secuencia y nombralos como  Actitudinales. "
                " 5. Genera el problema auténtico generador del proceso de enseñanza y aprendizaje (El problema deberá ser de contexto real o disciplinar). Deberás colocar el proceso detallado para solucionar el problema auténtico.  Nómbralo como Problema auténtico: "
                " El orden en que deberás presentarla se te da a continuación: "
                f" Título de la secuencia usando el texto: Título: {titulo}, "
                " Resumen: "
                " Palabras clave:"
                " Objetivos: "
                " Contenidos Conceptuales: "
                " Contenidos Procedimentales: "
                " Contenidos Actitudinales: "
                " Problema Auténtico: "
                )
                st.write('Prompt completo: ' + prompt)

                response = model.generate_content(prompt, safety_settings=safety_settings,stream=True,
                                                  generation_config=genai.types.GenerationConfig(
                                                  candidate_count=1,
                                                  temperature=0.7)
                                                  )
                for chunk in response:
                    st.markdown ( chunk.text )                
            except Exception as e :
                st.error ( 'Ha ocurrido un error con el siguiente mensaje: ' )
                st.write(e)