import streamlit as st
from langchain_groq import ChatGroq
from langchain.chains import LLMMathChain,LLMChain
from langchain_community.utilities import WikipediaAPIWrapper
from langchain.prompts import PromptTemplate
from langchain.agents.agent_types import AgentType
from langchain.agents import Tool, initialize_agent
from langchain.callbacks import StreamlitCallbackHandler

#Setup up the streamlit app
st.set_page_config(page_title="Text To math problem solver")
st.title("Text to Math Problem Solver using Google Gemma2")

groq_api_key=st.sidebar.text_input(label="Groq API Key",type="password")

if not groq_api_key:
    st.info("Please Add your Groq API Key to continue")

llm=ChatGroq(model="Gemma-9b-It",groq_api_key=groq_api_key)

