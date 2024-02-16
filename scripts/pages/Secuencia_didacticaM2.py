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
st.set_page_config(page_title="Secuencia Didáctica M2", page_icon="📃",layout="wide")
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
        autor=st.text_input('Autor:')
        adscripcion=st.text_input('Adscripción:')
        grado=st.text_input('Grado: ')
        nivel=st.text_input('Nivel educativo: ')
        fecha_entrega=st.date_input(format="DD/MM/YYYY",label="Entrega")
        fecha_aplicacion=st.date_input(format="DD/MM/YYYY",label="Aplicacion")
    with col2:
        st.header("Datos asignatura")
        materia=st.text_input('Materia')
        tema=st.text_input('Tema')
        alumnos=st.number_input('Número de alumnos a los que se aplica:', min_value=1, step=1)
        sesiones=st.number_input('Número de sesiones:', min_value=1, step=1)
        horas=st.number_input('Duración por sesión: (hora/clase)',min_value=1,step=1)
        metodologia=st.selectbox('Seleccione la metodología',("Gamificación","Aprendizaje Basado en Problemas"))
              
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
                f"Actua como docente genera una secuencia didáctica sobre {materia} para nivel {nivel} del grado {grado} "
                f" con tema {tema} usando la metodología {metodologia}. "
                " Deberás generar los siguientes apartados y nombrarlos como se indica en cada uno: "
                " 1. Genera objetivos de la secuencia didáctica y nombralos Objetivos. "
                " 2. Contenidos conceptuales que apoyará la secuencia y nómbralos como Conceptuales. "
                " 3. Contenidos procedimentales que apoyará la secuencia y nombralos como Procedimentales. "
                " 4. Contenidos actitudinales en el alumno que apoyará la secuencia y nombralos como  Actitudinales. "
                " 5. Problema auténtico generador del proceso de enseñanza y aprendizaje (de contexto real o disciplinar y nombralo como Problema auténtico): "
                " El orden en que deberás presentarla se te da a continuación y deberás dejar un renglón vacío entre cada uno de los apartados: "
                f" Título de la secuencia usando el texto: Título: {titulo}, "
                f" Autores: {autor}, "
                f" Adscripción: {adscripcion}. "
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