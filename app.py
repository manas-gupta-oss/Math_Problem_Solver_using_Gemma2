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

#Initializing the tools
wikipedia_wrapper=WikipediaAPIWrapper()
wikipedia_tool=Tool(
    name="Wikipedia",
    func=wikipedia_wrapper.run,
    description="Useful for when you need to answer questions about current events or general knowledge. Input should be a fully formed question."
)

#Initialize the math tool
math_chain=LLMMathChain.from_llm(llm=llm,verbose=True)
calculator=Tool(
    name="Calculator",
    func=math_chain.run,
    description="Useful for when you need to answer questions about math. Input should be a fully formed question."
)

prompt='''You are a math problem solver. You will be given a text description of a math problem, and you need to convert it into a mathematical expression or equation that can be solved. Your task is to identify the relevant information from the text and formulate it into a clear and concise mathematical representation. Please provide the final answer as well as the steps taken to arrive at that answer. If the problem cannot be solved, please explain why.'''

prompt_template=PromptTemplate(
   input_variables=["question"]
    template=prompt
)

#combining the tools into chain
chain=LLMChain(llm=llm,prompt=prompt_template)

reasoning_tool=Tool(
    name="Reasoning Tool",
    func=chain.run,
    description="Useful for when you need to reason through a problem and come up with a solution. Input should be a fully formed question."
)

#initialize the agent with the tools
assistant_agent=initialize_agent(
tools=[wikipedia_tool,calculator,reasoning_tool],
llm=llm,
agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
verbose=False,
handle_parsing_errors=True)

if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "assistant", "content": "You are a helpful assistant."}
    ]

for message in st.session_state.messages:
    st.chat_message(message["role"]).write(message["content"])

#function to generate the response 
def generate_response(question):
   response=assistant_agent.invoke({'input':question})

#Starting the chat interface
question=st.text_Area("Enter your math problem here:",key="input")

if st.

