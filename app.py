import streamlit as st
import random
import time
from src.prompts import get_initial_message
from src.user import User
from src.router import get_response
from src.util import typing_effect, add_chat_session_details, add_user_session_details


# Intialize user
if "user" not in st.session_state:
    st.session_state.user = User("John", 30)
    
# Initialize claim_form
if "claim_form_enabled" not in st.session_state:
    st.session_state.claim_form_enabled = False 


# using columns place a logo on the top right side of the page

col1, col2, col3 = st.columns([2, 6, 2])

with col3:
    st.image("logo.png", width=100)
    st.write("")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"], unsafe_allow_html=True)
        

# Initial message from assistant
if len(st.session_state.messages) == 0:
    full_response =  get_initial_message(st)
    st.session_state.messages.append({"role": "assistant", "content": full_response})

         

# Custom CSS style for the scrollable cards
st.markdown(
    """
    
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.1/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-4bw+/aepP/YC94hEpVNVgiZdgIC5+VKNBQNGCHeKRQN+PtmoHDEXuppvnDJzQIu9" crossorigin="anonymous">
    
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.1/dist/js/bootstrap.bundle.min.js" integrity="sha384-HwwvtgBNo3bZJJLYd8oVXjrBZt8cqVSpeBNS5n7C8IVInixGAoxmnlMuBnhbgrkm" crossorigin="anonymous"></script>
    
    <style>
    .scrollable-card-container {
        display: flex;
        max-width: 100%; /* Adjust the max width as needed */
        overflow-x: auto;
    }
    .scrollable-card {
        flex: 0 0 auto;
        padding: 10px;
        margin: 5px;
        border: 1px solid lightgray;
        border-radius: 5px;
        box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.1);
    }
    </style>
    
    """,
    unsafe_allow_html=True,
)



# Accept user input
chat_input = st.chat_input("Type your message here...")
if prompt := chat_input:
    # Add user message to chat history
    add_user_session_details(st, prompt)
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt, unsafe_allow_html=True)

    # Display assistant response in chat message container
    get_response(prompt, st.session_state.user, st, chat_input)  
    
    
# Display claim form
if st.session_state.claim_form_enabled:
    file_uploader = st.file_uploader("Kindly upload your filled claim form here", type=["pdf", "png", "jpg"])
    
    
    if file_uploader:
         # Display user message in chat message container
        add_user_session_details(st, f"User uploaded claim form {file_uploader.name}")
        
        st.session_state.user.claim_form = file_uploader
        
        response = "Your claim form has been successfully uploaded. You can also let me know if you have any queries on your claim."
        add_chat_session_details(st, response)
        typing_effect(st, response)
        
        st.session_state.claim_form_enabled = False
        
        
       
            
     
      
    
    
    
    
    
