import streamlit as st
import os
import google.generativeai as genai
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_community.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate


st.set_page_config(page_title="Chatea con PDF's", page_icon="📃",layout="wide")
st.markdown("# Pregunta sobre tu PDF")
st.sidebar.header("Chat con PDF's")
st.write(
    """Chat with PDF's"""
)
with st.sidebar:
    pdf_docs=st.file_uploader("upload your PDF")

try:
   genai.configure(api_key=st.session_state.app_key)
except AttributeError as e:
    st.warning("Introduzca primero su clave API")
modelai=genai.GenerativeModel('gemini-pro')

os.environ['GOOGLE_API_KEY']=st.session_state.app_key
def get_pdf_text(pdf_docs):
    text=" "
    for pdf in pdf_docs:
        pdf_reader=PdfReader(pdf)
        for page in pdf_reader.pages:
            text+=page.extract_text()
    return text

def get_text_chunks(text):
    text_splitter=RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=1000)
    chunks=text_splitter.split_text(text)
    return chunks

def get_vector_store(text_chunks):
    embeddings=GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    vector_store=FAISS.from_texts(text_chunks,embedding=embeddings)
    vector_store.save_local("faiss_index")

def get_conversational_chain():
    prompt_template=""" 
    Responde la pregunta tan detallada como sea posible desde el contexto provisto, asegúrate de proveer todos los detalles, si la respuesta no está 
    en el contexto provisto, solo responde "Respuesta no disponible en el contexto", no des una respuesta incorrecta \n\n
    Contexto: \n{context}?\n
    Question: n{question}\n

    Respuesta:
    """
    model=ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.3, google_api_ket=st.session_state.app_key)
    prompt=PromptTemplate(template=prompt_template, input_variables=["context","question"])
    chain=load_qa_chain(model,chain_type="stuff",prompt=prompt)
    return chain

def user_input(user_question):
    embeddings=GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    new_db=FAISS.load_local("faiss_index",embeddings, allow_dangerous_deserialization=True)
    docs=new_db.similarity_search(user_question)
    chain=get_conversational_chain()

    response=chain(
        {"input_documents":docs,"question":user_question}
        ,return_only_outputs=True)
    
    print(response)
    st.write("Reply: ", response["output_text"])

user_question=st.text_input("Ask a question from the PDF file")
if user_question:
    user_input(user_question)
    if st.button("Submit & Process"):
        with st.spinner("Processing..."):
            raw_text=get_pdf_text(pdf_docs)
            text_chunks=get_text_chunks(raw_text)
            get_vector_store(text_chunks)
            st.success("Done")

