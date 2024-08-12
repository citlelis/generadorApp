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
        grado=st.text_input('Grado: ', value= "Primero")
        nivel=st.text_input('Nivel educativo: ', value= "Preparatoria")
    with col2:
        st.header("Datos asignatura")
        materia=st.text_input('Materia', value="Física")
        tema=st.text_input('Tema')
        #alumnos=st.number_input('Número de alumnos a los que se aplica:', min_value=1, step=1)
        sesiones=st.number_input('Número de sesiones:', min_value=1, step=1)
        horas=st.number_input('Duración por sesión: (hora/clase)',min_value=1,step=1)
        metodologia=st.selectbox('Seleccione la metodología',("Gamificación","Aprendizaje Basado en Problemas","Aula Invertida"))
    with col3:
        st.header("Personalización")
        competencia=st.text_area('Escriba brevemente la competencia que debe adquirir el estudiante')
        aprend_esperado=st.text_input('Escriba brevemente el aprendizaje esperado')
    submit= st.form_submit_button('Generar')
#Fin forma

data=""

#Se ha presionado en botón de Generar
if submit:
    with st.container () :
        with st.spinner ( 'Espere mientras Gemini genera la respuesta...' ) :
            try :
                prompt=(
                f" Como docente experto de Bachillerato, "
                f" crea una secuencia didáctica para jóvenes entre 15 y 18 años, de la materia {materia}, "
                f" sobre el tema {tema}, para nivel {nivel} del grado {grado},"
                 " basada en la teoría del aprendizaje significativo de David Ausubel."
                f" Usa la metodología {metodologia} " 
                 " Asegúrate de: "
                 " considerar las estructuras cognitivas previas, "
                 " utiliza inclusores que conecten la nueva información con lo ya conocido, "
                 " usar inclusores para conectar la nueva información con lo ya conocido,  "
                 " proporcionar instrucciones claras para  el anclaje,  "
                 " evalúa cómo la nueva información modifica la estructura cognitiva de los estudiantes, "
                 f"estructura la secuencia en {sesiones} sesiones, cada una con inicio, desarrollo y cierre. "
                 f" Si se han proporcionado, integra las siguientes competencias y aprendizajes esperados: "
                 f" Competencias: {competencia}. "
                 f" Aprendizaje esperado: {aprend_esperado}. "
                  " Incluye un plan de evaluación formativa y sumativa. "
                 " Presenta la secuencia con los siguientes apartados : "
                f" Título de la secuencia: {titulo}, "
                 " Resumen: "
                 " Palabras clave:"
                 " Contenidos Conceptuales: 3 elementos "
                 " Contenidos Procedimentales: 3 elementos "
                 " Contenidos Actitudinales: 3 elementos "
                 " Cuestionario para activar conocimientos previos con 5 preguntas de exploración "
                 " Problema Auténtico: Contextualizado en la Ciudad de México, significativo "
                 " y detallado con el proceso de solución."
                 " Plan de evaluación: "
                )
                st.write('Prompt completo: ' + prompt)

                response = model.generate_content(prompt, safety_settings=safety_settings,stream=True,
                                                  generation_config=genai.types.GenerationConfig(
                                                  candidate_count=1,
                                                  temperature=0.7)
                                                  )
                for chunk in response:
                    data+= chunk.text
                st.markdown(data)
                    #st.markdown ( chunk.text )                
            except Exception as e :
                st.error ( 'Ha ocurrido un error con el siguiente mensaje: ' )
                st.write(e)