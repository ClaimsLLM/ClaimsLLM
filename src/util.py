import time
def typing_effect(st, message):
    with st.chat_message("assistant"):
        message_placeholder = st.markdown("")
        curr_response = ""
        for chunk in message.split():
            curr_response += chunk + " "
            time.sleep(0.05)
            # Add a blinking cursor to simulate typing
            message_placeholder.markdown(curr_response + "▌")
        
        message_placeholder.markdown(message)

def add_chat_session_details(st , object):
    st.session_state.messages.append({"role": "assistant", "content": object}) 
    
def add_user_session_details(st , object):
    st.session_state.messages.append({"role": "user", "content": object})
     
     
    