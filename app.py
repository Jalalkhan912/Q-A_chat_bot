import streamlit as st
from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate


import os
from dotenv import load_dotenv

load_dotenv()

## Langsmith Tracking
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")
os.environ["LANGCHAIN_TRACKING_V2"]="true"
os.environ["LANGCHAIN_PROJECT"] = os.getenv("LANGCHAIN_PROJECT")
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")

## prompt Template
prompt = ChatPromptTemplate(
    [
        ("system","You are a helpful assisstant. Please response to the user queries"),
        ("user","Questions:{questions}")
    ]
)

def generate_response(question,llm):
    llm = ChatGroq(model=llm)
    output_parser = StrOutputParser()
    chain = prompt|llm|output_parser
    answer = chain.invoke({'questions':question})
    return answer

## Title of the app
st.title("Q&A Chatbot with Groq")

## sidebar for settings
st.sidebar.title("Settings")

## Drop down to select various Groq models
llm=st.sidebar.selectbox("Select Groq Model",["llama3-8b-8192","llama3-70b-8192"])

## Main interface for user input
st.write("Ask freely, if you have any Question")
user_input = st.text_input("You:")

if user_input:
    response=generate_response(user_input, llm)
    st.write(response)
else:
    st.write("Please provide the question")
