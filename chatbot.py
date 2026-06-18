#from dotenv import load_dotenv
# used to create the Web UI
import streamlit as st

#Langchain wrapper around GROQ's LLM API
from langchain_groq import ChatGroq

# Load the environment variable
#load_dotenv()

# Streamlit page setup

st.set_page_config(
    page_title="💬 Chatbot",
    page_icon="🤖",
    layout="centered"
)

st.title("Generative AI chatbot")

# Streamlit reruns the entire script whenever "button clicked","user types" and "page refreshed",
# without session state, chat_history[] would become empty every rerun
# Initiate chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Show chat history
#loop through every stored message , for each message , create a chat bubble
for message in st.session_state.chat_history:
    # create user bubble or assistant bubble
    with st.chat_message(message["role"]):
        #display message
        st.markdown(message["content"])

# llm initiate or create LLM, create a connection to GROQ
llm = ChatGroq(
    model = "llama-3.3-70b-versatile", # Large Meta Llama model hosted by Groq.
    temperature=0.0,
)
# Create the input box
user_prompt = st.chat_input("Ask Chatbot .....")

# Run only when user submitted a message

if user_prompt:
    st.chat_message("user").markdown(user_prompt) # show user message
    # Store user message
    st.session_state.chat_history.append({"role": "user","content":user_prompt}) 
    
    #call llm , this is most important part
    # What is sent?


# * operator

# This is Python unpacking.
#a = [1,2,3]

# [0,*a]

# becomes:
# [0,1,2,3]
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



