#APP PARA MIDIEMS
#AUTOR: CILG AÑO: 2024
#SECUENCIA DIDÁCTICA MODELO M2

import streamlit as st
import google.generativeai as genai
from fpdf import FPDF
import base64
from datetime import datetime
from unidecode import unidecode

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
        sesiones=st.number_input('Número de sesiones:', min_value=1, step=1)
        horas=st.number_input('Duración por sesión: (hora/clase)',min_value=1,step=1)
        metodologia=st.selectbox('Seleccione la metodología',("Gamificación","Aprendizaje Basado en Problemas","Aula Invertida","Microaprendizaje","Otro"))        
    with col3:
        st.header("Personalización")
        competencia=st.text_area('Escriba brevemente la competencia que debe adquirir el estudiante',height=100)
        aprend_esperado=st.text_area('Escriba brevemente el aprendizaje esperado',height=100)
        estilo_aprendizaje =st.selectbox(' Seleccione el estilo de aprendizaje',("Activo o divergente", "Reflexivo o asimilador", "Teórico o convergente","Pragmático o acomodador"))
    submit= st.form_submit_button('Generar')
#Fin forma

data=""

#Se ha presionado en botón de Generar
if submit:
    with st.container () :
        with st.spinner ( 'Espere mientras Gemini genera la respuesta...' ) :
            try:
                prompt=(
                 " Eres un docente de Bachillerato en México,"
                 " experto en el diseño instruccional y hábil en el diseño de secuencias didácticas, " 
                 " y con amplio conocimiento de la teoría  de aprendizaje significativo de David Ausubel. "
                f" Debes generar una secuencia didáctica para estudiantes entre 15 y 18 años, de la materia {materia}, "
                f" sobre el tema {tema}, para nivel {nivel} del grado {grado}, la situación problemática será {situacion}. "
                f" Usa la metodología {metodologia}.  " 
                 " La secuencia didáctica debe estar diseñada bajo los principios del aprendizaje significativo, considerando los siguientes elementos: "
                 " Incluye un organizador previo que será un párrafo que permita a los estudiantes conectar el nuevo conocimiento con sus ideas o experiencias previas, "
                 " Diseña actividades que permitan a los estudiantes activar y relacionar sus conocimientos previos con el nuevo contenido, "
                 " Estructura el contenido de manera que se presente desde lo más general y simple hacia lo más específico y complejo, permitiendo una comprensión gradual y profunda, "
                 " utiliza inclusores que conecten la nueva información con lo ya conocido, "
                 " proporciona instrucciones claras para  el anclaje.  "
                 f" Estructura la secuencia en {sesiones} sesiones, cada una con inicio, desarrollo y cierre. "
                 f" Si se han proporcionado, integra las siguientes competencias, aprendizajes esperados y estilo de aprendizaje: "
                 f" Competencias: {competencia}. "
                 f" Aprendizaje esperado: {aprend_esperado}. "
                 f" Estilo de aprendizaje: {estilo_aprendizaje}, de acuerdo con la teoría de Kolb."
                  " Incluye un plan de evaluación formativa y sumativa que permitan verificar una comprensión significativa del tema. "
                  " La secuencia didáctica debe ser clara, estructurada y adaptada al nivel cognitivo y emocional de los estudiantes, promoviendo su participación activa y colaborativa así como el desarrollo de habilidades de pensamiento crítico y reflexivo."
                 " Presenta la secuencia con los siguientes apartados : "
                f" Título de la secuencia {titulo}, "
                 " Resumen. "
                 " Palabras clave."
                 " Cuestionario para activar conocimientos previos con 5 preguntas de exploración. "
                 " Problema Auténtico contextualizado y significativo segun la situación problemática referida"
                 " el problema debe estar detallado, debiendo incluir el proceso de solución."
                 " Plan de evaluación. "
                 " Recursos, en el que deberás indicar autores, enlaces y publicaciones relevantes a considerar. "
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
                
                #Impresion PDF
                if data:
                    pdf=FPDF()
                    pdf.add_page()
                    try:
                        pdf.add_font('DejaVu', '', 'DejaVuSans.ttf', uni=True)
                        pdf.set_font('DejaVu', '', 12)
                    except:
                        pdf.set_font("Arial", size=12)   
                    
                    pdf.set_title(titulo[:100])  # Limitar longitud
                    pdf.set_author("App para el docente")
                    
                    
                    pdf.set_font('Arial', 'B', 16)
                    pdf.cell(200, 10, txt=titulo[:100], ln=1, align='C')
                    pdf.ln(10)

                    #Data general
                    pdf.set_font('Arial','',12)
                    pdf.cell(200, 10, txt=f"Materia: {materia}",ln=1)
                    pdf.cell(200, 10, txt=f"Grado: {grado} - Nivel: {nivel}", ln=1)
                    pdf.cell(200, 10, txt=f"Tema: {tema}", ln=1)
                    pdf.cell(200, 10, txt=f"Metodología: {metodologia}", ln=1)
                    pdf.ln(15)


                    pdf.set_font('Arial','',size=12)
                    #Data generada
                    try:
                        for line in data.split('\n'):
                            if line.strip():
                                safe_line=unidecode(line)
                                pdf.multi_cell(0,10,txt=safe_line)
                                pdf.ln(5)    
                    except Exception as e:
                        st.error("Error al generar el archivo PDF")

                    #Fecha y hora
                    pdf_bytes=pdf.output(dest='S').encode('latin-1','replace')
                    timestamp =datetime.now().strftime("%d%m%Y_%H%M%S")
                    filename=f"secuencia_{titulo[:20]}_{timestamp}.pdf".replace(" ","_")

                    #Guadado temporal
                    #pdf.output=pdf.output(dest='S').encode('latin-1','replace')

                    
                    #Enlace para descarga
                    st.download_button(
                        label="Descargar PDF",
                        data=pdf_bytes,
                        file_name=filename,
                        mime="application/pdf"
                    )

            except Exception as e :
                st.error ( 'Ha ocurrido un error con el siguiente mensaje: ' )
                st.write(e)