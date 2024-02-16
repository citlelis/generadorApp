import streamlit as st
import google.generativeai as genai


st.set_page_config(page_title="Secuencia Didáctica", page_icon="📈")

st.markdown("# Generador de secuencias didácticas")
st.sidebar.header("Secuencia Didáctica")
st.write(
    """App para generar secuencias didácticas"""
)

try:
    genai.configure(api_key=st.session_state.app_key)
except AttributeError as e:
    st.warning("Introduzca primero su clave API")
model=genai.GenerativeModel('gemini-pro')


#Forma
my_form=st.form(key='form-1')
rol=my_form.text_input('Rol: ')
titulo=my_form.text_input('Título de secuencia: ')
autor=my_form.text_input('Autor:')
adscripcion=my_form.text_input('Adscripción:')
grado=my_form.text_input('Grado: ')
sesiones=my_form.text_input('Número de sesiones:')
horas=my_form.text_input('Duración por sesión:')
alumnos=my_form.number_input('Número de alumnos a los que se aplica:')
metodologia=my_form.selectbox('Seleccione la metodología',("Gamificación","ABP"))
nivel=my_form.text_input('Nivel: ')
materia=my_form.text_input('Materia')
tema=my_form.text_input('Tema')
fecha_entrega=my_form.date_input(format="DD/MM/YYYY",label="Entrega")
fecha_aplicacion=my_form.date_input(format="DD/MM/YYYY",label="Aplicacion")
recurso=my_form.selectbox('Seleccione su recurso a generar',("Lección","Presentación","Secuencia didáctica","Línea de tiempo" ))   
submit= my_form.form_submit_button('Generar')
#Fin forma

#if "app_key" in st.session_state:
st.write('Nivel es: ' + nivel)
st.write('Materia: '+ materia)
st.write('Tema: ' + tema)
st.write('Recurso: ',recurso)

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



if submit:
    with st.container () :
        with st.spinner ( 'Espere mientras Gemini genera la respuesta...' ) :
            try :
                prompt=(
                f"Actua como {rol} genera {recurso} sobre {materia} para nivel {nivel} del grado {grado} "
                f" con tema {tema} usando la metodología {metodologia}. "
                " Deberás generar los siguientes apartados y nombrarlos como se indica en cada uno: "
                " 1. Genera un resumen muy breve de dos líneas sobre lo generado y nombralo Resumen. "
                " 2. Agrega 5 palabras clave sobre lo generado y nómbralo Palabras clave."
                " 3. Agrega una introducción del contexto donde abordes a problemática educativa, "
                " especifica qué resuelve la secuencia propuesta, indicando sus objetivos para el desarrollo de una habilidad y señalando su justificación, todo en un máximo de 6 renglones "
                " a este apartado le nombrarás  Introducción del contexto. "
                " 4. Agrega un apartado donde expliques la Temática, que debe incluir aprendizajes, propósitos y problema que atiende a este apartado le nombrarás Temática. "
                " El orden en que deberás presentarla se te da a continuación y deberás dejar un renglón vacío entre cada uno de los apartados: "
                f" Título de la secuencia usando el texto: Título: {titulo}, "
                f" Autores: {autor}, "
                f" Adscripción: {adscripcion}. "
                " Resumen: "
                " Palabras clave:"
                " Introducción del contexto: "
                "Temática: "

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
                