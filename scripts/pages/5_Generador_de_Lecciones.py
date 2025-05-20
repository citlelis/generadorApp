#APP PARA MIDIEMS
#AUTOR: CILG AÑO: 2024
#GENERADOR DE LECCIONES GENÉRICO

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
st.set_page_config(page_title="Generador de Lecciones", page_icon="📃",layout="wide")
st.markdown("# Generador de Lecciones (Genérico) ")
st.sidebar.header("Generador de Lecciones (Genérico)")
st.write(
    """App para generar lecciones"""
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
        titulo=st.text_input('Título de la lección: ')
        grado=st.text_input('Grado: ')
        nivel=st.text_input('Nivel educativo: ')
    with col2:
        st.header("Datos asignatura")
        materia=st.text_input('Materia')
        tema=st.text_input('Tema')
        alumnos=st.number_input('Número de alumnos a los que se aplica:', min_value=1, step=1)
        metodologia=st.selectbox('Seleccione la metodología',("Gamificación","Aprendizaje Basado en Problemas","Aula Invertida", "Constructivista"))
              
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
                f"Actua como docente de Bachillerato. Diseña una clase sobre {tema}, para alumnos de entre 15 y 18 años, de nivel {nivel} del grado {grado},"
                f" usando la metodología {metodologia}. El esquema detallado para el plan de lección es: "
                " Objetivos: Identificar claramente lo que se espera que los estudiantes aprendan al final de la lección. "
                " Establecer metas alcanzables y relevantes para su nivel y grado académico. "
                " Materiales: Enumerar todos los recursos necesarios para llevar a cabo la lección de manera efectiva."
                " Introducción: Proporcionar una descripción atractiva del tema para captar el interés de los estudiantes y "
                " Relacionar el tema con experiencias previas o situaciones del mundo real para una mejor comprensión."
                " Procedimeinto: Desglosar las actividades paso a paso que se llevarán a cabo para lograr los objetivos de la lección e  "
                " Incluir métodos de enseñanza interactivos y variados para mantener el compromiso y la participación de los estudiantes." 
                " Evaluación: Diseñar un cuestionario que evalúe de manera efectiva si se han alcanzado los objetivos de aprendizaje."
                " e incluir  en dicho cuestionario una combinación de preguntas de opción múltiple, verdadero o falso, y preguntas abiertas para evaluar diferentes niveles de comprensión."
                " Conclusión: un resumen de la lección con los puntos clave y su relevancia para el aprendizaje futuro. "
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