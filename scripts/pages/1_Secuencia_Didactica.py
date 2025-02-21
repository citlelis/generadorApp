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
model=genai.GenerativeModel('gemini-2.0-flash')

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
        situacion=st.text_input('Situación problemática')
        #alumnos=st.number_input('Número de alumnos a los que se aplica:', min_value=1, step=1)
        sesiones=st.number_input('Número de sesiones:', min_value=1, step=1)
        horas=st.number_input('Duración por sesión: (hora/clase)',min_value=1,step=1)
        metodologia=st.selectbox('Seleccione la metodología',("Gamificación","Aprendizaje Basado en Problemas","Aula Invertida"))
    with col3:
        st.header("Personalización")
        competencia=st.text_area('Escriba brevemente la competencia que debe adquirir el estudiante')
        aprend_esperado=st.text_input('Escriba brevemente el aprendizaje esperado')
        estilo_aprendizaje =st.selectbox(' Seleccione el estilo de aprendizaje',("Activo o divergente", "Reflexivo o asimilador", "Teórico o convergente","Pragmático o acomodador"))
    submit= st.form_submit_button('Generar')
#Fin forma

data=""

#Se ha presionado en botón de Generar
if submit:
    with st.container () :
        with st.spinner ( 'Espere mientras Gemini genera la respuesta...' ) :
            try :
                prompt=(
                 " Eres un docente de Bachillerato en México,"
                 " experto en el diseño instruccional y hábil en el diseño de secuencias didácticas, " 
                 " y con amplio conocimiento de la teoría  de aprendizaje significativo de David Ausubel. "
                f" Debes generar una secuencia didáctica para jóvenes entre 15 y 18 años, de la materia {materia}, "
                f" sobre el tema {tema}, para nivel {nivel} del grado {grado}, la situación problemática será {situacion}. "
                f" Usa la metodología {metodologia}.  " 
                 " La secuencia didáctica debe estar diseñada bajo los principios del aprendizaje significativo, considerando los siguientes elementos: "
                 " Incluye una actividad introductoria que funcione como organizador previo, permitiendo a los estudiantes conectar el nuevo conocimiento con sus ideas o experiencias previas, "
                 " Diseña actividades que permitan a los estudiantes activar y relacionar sus conocimientos previos con el nuevo contenido, facilitando la asimilación significativa, "
                 " Estructura el contenido de manera que se presente desde lo más general y simple hacia lo más específico y complejo, permitiendo una comprensión gradual y profunda, "
                 " Incluye actividades que fomenten la integración de conceptos, promoviendo la comparación, el contraste y la síntesis de ideas para lograr una comprensión holística, "
                 " utiliza inclusores que conecten la nueva información con lo ya conocido, "
                 " proporcionar instrucciones claras para  el anclaje,  "
                 " evalúa cómo la nueva información modifica la estructura cognitiva de los estudiantes, "
                 f" estructura la secuencia en {sesiones} sesiones, cada una con inicio, desarrollo y cierre. "
                 f" Si se han proporcionado, integra las siguientes competencias, aprendizajes esperados y estilo de aprendizaje: "
                 f" Competencias: {competencia}. "
                 f" Aprendizaje esperado: {aprend_esperado}. "
                 f" Estilo de aprendizaje: {estilo_aprendizaje}, de acuerdo con la teoría de Kolb."
                  " Incluye un plan de evaluación formativa y sumativa que permitan verificar una comprensión significativa del tema. "
                  " La secuencia didáctica debe ser clara, estructurada y adaptada al nivel cognitivo y emocional de los estudiantes, promoviendo su participación activa y colaborativa así como el desarrollo de habilidades de pensamiento crítico y reflexivo."
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