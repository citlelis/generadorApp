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
model=genai.GenerativeModel('gemini-2.0-flash')
if "chat" not in st.session_state:
    st.session_state.chat = model.start_chat( history = [])
st.title("Mi Asistente")
st.write("Presione una opción o escriba su petición en el chat")
col1, col2, col3=st.columns(3)
with col1:
    st.write("Evaluación")
    b1=st.button('Prompt para Evaluación Auténtica')
    b2=st.button('Prompt para Generar Cuestionarios')
with col2:
    st.write("Comportamiento y Rompehielos")
    b3=st.button('Prompt para Intervención de Comportamiento')
    b4=st.button('Prompt para Actividades Rompehielos')
with col3:
    st.write("Mis estudiantes")
    b5=st.button('Prompt para Explicar y simplificar temas')
    b6=st.button('Prompt Actividades Cooperativas de Aprendizaje')
if b1:
    st.session_state.chat = model.start_chat( history = [])
    txt= st.text_area("Edite el siguiente prompt, modificando los parámetros en mayúsculas. Al terminar copie y pegue su petición.","Eres un docente experto, hábil en desarrollar evaluaciones auténticas innovadoras y efectivas que permitan a los estudiantes desarrollar y mostrar su aprendizaje. Tu tarea es crear [NÚMERO] evaluaciones auténticas [FORMATIVAS O SUMATIVAS] para mi clase de [NIVEL DE GRADO Y MATERIA] que está estudiando [TEMA]. Las evaluaciones deben medir el [ESTÁNDAR DE CONTENIDO]. Éstas deben enfatizar la aplicación en el mundo real, tareas complejas, formatos de respuesta variados y retroalimentación significativa. [OPCIONAL SI ES SUMATIVA: INCLUYA LA VERIFICACIÓN DE QUE SE ALCANZÓ EL ESTÁNDAR]. Las evaluaciones [FORMATIVAS O SUMATIVAS] deben involucrar a los estudiantes y demostrar de manera efectiva su aprendizaje, así como mejorar sus habilidades y comprensión de la materia de manera significativa. Sé creativo y único, no [INCLUIR CUALQUIER ESPECIFICACIÓN RESTANTE].",)
if b2:
    st.session_state.chat = model.start_chat( history = [])
    txt=st.text_area("Edite el siguiente prompt, modificando los parámetros en mayúsculas. Al terminar copie y pegue su petición","Eres un docente experto, hábil en la creación de evaluaciones detalladas para estudiantes que demuestren efectivamente su aprendizaje. Tu tarea es crear un [TIPO] de evaluación para estudiantes de [GRADO Y MATERIA] que estén aprendiendo sobre [TEMA]. Incluye [HABILIDADES A EVALUAR]. Proporciona una clave de respuestas para el docente.",)
if b3:
    st.session_state.chat = model.start_chat( history = [])
    txt=st.text_area("Edite el siguiente prompt, modificando los parámetros en mayúsculas. Al terminar copie y pegue su petición","Eres un experto maestro de [ESCUELA SECUNDARIA / ESCUELA PREPARATORIA] con habilidades en el uso de estrategias de manejo e intervención informadas por el desarrollo para mantener un ambiente de aprendizaje en el aula tranquilo y equilibrado. Tu tarea es desarrollar un proceso específico de respuesta conductual para tu estudiante de [NIVEL DE GRADO Y ASIGNATURA] que exhibe [INSERTAR COMPORTAMIENTOS ESPECÍFICOS] cuando [INSERTAR INFORMACIÓN ESPECÍFICA DE LA SITUACIÓN]",)
if b4:
    st.session_state.chat=model.start_chat(history=[])
    txt=st.text_area("Edite el siguiente prompt, modificando los parámetros en mayúsculas. Al terminar copie y pegue su petición","Eres un experto educador y diseñador instruccional con profunda experiencia en el campo del aprendizaje socioemocional para estudiantes Preparatoria. Te especializas en crear actividades de rompehielos atractivas, interactivas y divertidas que los educadores pueden utilizar con los estudiantes para construir relaciones entre maestros y alumnos, fomentar conexiones entre compañeros y desarrollar habilidades socioemocionales clave. Tu tarea es crear una breve actividad de rompehielos que pueda ser facilitada en un tiempo de [NÚMERO] minutos, enfocada en [HABILIDAD SOCIOEMOCIONAL] para estudiantes de [NIVEL DE GRADO], con edades entre [EDADES].")
if b5:
    st.session_state.chat=model.start_chat(history=[])
    txt=st.text_area("Edite el siguiente prompt, modificando los parámetros en mayúsculas. Al terminar copie y pegue su petición","Eres un docente experto con excelentes habilidades de comunicación e interpersonales, especialmente hábil en simplificar y reformular temas complicados para audiencias específicas. Tu tarea es explicar el concepto de [TEMA COMPLEJO] en términos simples, para que mi clase de [NIVEL DE GRADO Y ASIGNATURA] pueda entender [CONCEPTO / EJEMPLO ESPECÍFICO].",)
if b6:
    st.session_state.chat=model.start_chat(history=[])
    txt=st.text_area("Edite el siguiente prompt, modificando los parámetros en mayúsculas. Al terminar copie y pegue su petición ","Eres un experto educador y diseñador instruccional con amplio conocimiento de estrategias de aprendizaje socioemocional y del marco Colaborativo para el aprendizaje académico social y emocional (CASEL). Tu tarea es crear un proyecto de aprendizaje cooperativo para mi clase de [NIVEL DE GRADO] basado en nuestra unidad de [ASIGNATURA] sobre [RESUMEN DE LA UNIDAD / OBJETIVOS DE LA LECCIÓN]. Incluye estrategias específicas para ayudar a los estudiantes a desarrollar relaciones positivas con miembros diversos del grupo y fomentar la colaboración, la comunicación y el trabajo en equipo.",)
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



