from dotenv import load_dotenv
import streamlit as st

from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq
from langchain_ollama import ChatOllama

load_dotenv()

st.set_page_config(
    page_title="Multi Model Chatbot",
    page_icon="🤖",
    layout="centered"
)
st.title("Multi-Model chatbot")
#-----------------------------
# Provider Selection
#-----------------------------

provider = st.sidebar.selectbox(
    "Choose Provider",
    ["OpenAI",'Gemini','Groq','Ollama']
)

models = {
    "OpenAI" : [
        "gpt-3.5-turbo",
        "gpt-4o"
    ],
    "Gemini" : [
        "gemini-2.5-flash",
        "gemini-2.5-pro"
    ],
    "Groq" : [
        "llama-3.1-8b-instant",
        "llama-3.3-70b-versatile"
    ],
    "Ollama": [
        "gemma2:2b"
    ]

}

selected_model = st.sidebar.selectbox(
    "Choose Model",
    models[provider]
)

#-----------------------------
# Session State --------------
# ----------------------------

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Display history

for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# ----------------------------------------------
# Create LLM

# -------------------------------------------

def get_llm(provider,model_name):

    if provider == "OpenAI":
        return ChatOpenAI(
            model = model_name,
            temperature=0.0

        )
    elif provider == "Gemini":
        return ChatGoogleGenerativeAI(
            model = model_name,
            temperature=0.0
        )
    elif provider == "Groq":
        return ChatGroq(
            model = model_name,
            temperature=0.0
        )
    elif provider == "Ollama":
        return ChatOllama(
            model = model_name,
            temperature= 0.0

        )
#----------------------------------
# Chat Input

# ----------------------------------

user_prompt = st.chat_input("Ask Something ......")

if user_prompt:
   st.chat_message("user").markdown(user_prompt)

   st.session_state.chat_history.append({"role":"user","content" : user_prompt})
   llm = get_llm(
        provider,
        selected_model
   )
   
   response = llm.invoke(
        input = [{"role":"system","content":"you are helpful assistant"},
                 *st.session_state.chat_history]
   ) 
    # Response Object
   assistant_response = response.content
    # Store Assistant Reply
   st.session_state.chat_history.append({"role":"assistant","content":assistant_response})
    
# Display Assistant Response
   with st.chat_message("assistant"):
       st.markdown(assistant_response)