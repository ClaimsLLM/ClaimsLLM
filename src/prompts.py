import streamlit
import time

def get_initial_message(st):
    with st.chat_message("assistant"):
        full_response = """
        Welcome to goML Claim Assistance. I am Claim X. I’m here to support you with
        """
        # 1. Policy Queries 2. Upload Claim Form and 3. Claim Queries.
        
        options = ["Policy Queries", "Upload Claim Form", "Claim Queries"]
        message_placeholder = st.markdown("")
        
        # simulate stream of response with milliseconds delay
        for chunk in full_response.split():
            full_response += chunk + " "
            time.sleep(0.05)
            # Add a blinking cursor to simulate typing
            message_placeholder.markdown(full_response + "▌")
        
        
        for i in range(len(options)):
            time.sleep(0.05)
            full_response += "\n" + str(i+1) + ". " + options[i]
            message_placeholder.markdown(full_response)
        
        full_response += "\n"
        message_placeholder.markdown(full_response)
            
        
        phone_response = """Please enter your phone number to continue."""
        
        full_response += "\n"
        
        for chunk in phone_response.split():
            full_response += chunk + " "
            time.sleep(0.05)
            # Add a blinking cursor to simulate typing
            message_placeholder.markdown(full_response + "")
            
        
        return full_response

# def get_(st):

    
    
    
        
         
        
        
    
