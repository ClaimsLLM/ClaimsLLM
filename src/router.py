from src.user import User
import re, time
from src.db_query import extract_data_to_json
from src.util import typing_effect, add_chat_session_details, add_user_session_details





def get_response(prompt:str, user:User, st, chat_input):
    # Check if prompt is a phone number string using regex
    if re.match(r"^\d{10}$", prompt):
        user.phone = prompt
        user.policy_details=extract_data_to_json(user.phone)
        print(user.policy_details)
        with st.chat_message("assistant"):
            message_placeholder = st.markdown("")
            full_response = "Thank you. Please wait while we verify your details."
            curr_response = ""
            for chunk in full_response.split():
                curr_response += chunk + " "
                time.sleep(0.05)
                # Add a blinking cursor to simulate typing
                message_placeholder.markdown(curr_response + "▌")
            
            message_placeholder.markdown(full_response)
            add_chat_session_details(st, full_response+"<br>")
            
            time.sleep(1)
            
            new_response = "We have found the following policies associated with your phone number."
            add_chat_session_details(st, new_response)
            
            message_placeholder.markdown(new_response)
            
                
            
            with st.container():
                st.markdown("<h2>Policy Information</h2>", unsafe_allow_html=True)
                
                # Create the scrollable card container
                scrollable_container = st.container()
                
                # Add the CSS class to the scrollable card container
                st.markdown('<div class="scrollable-card-container">', unsafe_allow_html=True)
                
                # Loop through the policies and create cards
                for policy in user.policy_details:
                    policy_card =   f"""
                        <div class="scrollable-card">
                            <h3>Policy Number: {policy['Policy Number']}</h3>
                            <p><b>Name:</b> {policy['Name']}</p>
                            <p><b>Mobile Number:</b> {policy['Mobile Number']}</p>
                            <p><b>Registration Number:</b> {policy['Registration Number']}</p>
                            <p><b>Sum Insured:</b> {policy['Sum Insured']}</p>
                            <p><b>Period of Insurance:</b> {policy['Period of Insurance']}</p>
                        </div>
                        """
                    policy_rep = st.markdown(
                      policy_card,
                        unsafe_allow_html=True,
                    )
                    add_chat_session_details(st, policy_card) 
                
                # Close the scrollable card container
                st.markdown('</div>', unsafe_allow_html=True)
                
                message = "Please select the policy number you would like to make a claim for."
                message_placeholder = st.markdown("")
                curr_response = ""
                for chunk in message.split():
                    curr_response += chunk + " "
                    time.sleep(0.05)
                    # Add a blinking cursor to simulate typing
                    message_placeholder.markdown(curr_response + "▌")
                
                message_placeholder.markdown(message)
                add_chat_session_details(st, message+"<br>")
                st.session_state.next_question = "policy_selection"
                
    
    elif prompt.startswith("P"):
        if prompt in [policy['Policy Number'] for policy in user.policy_details]:
            typing_effect(st, f"Please enter the query you would like to make for this policy. {prompt} ")
            user.selected_policy_no = prompt
            add_chat_session_details(st, f"Please enter the query you would like to make for this policy. {prompt} <br>")
            
    
    
    elif "claim" in prompt.lower() and "status" in prompt.lower():
        if not st.session_state.user.claim_form:
            response = "Kindly upload the claim form to check the status."
            
            typing_effect(st, response)
            add_chat_session_details(st, response+"<br>")
            
            st.session_state.claim_form_enabled = True
            
        else:
            response = "Your claim is currently being processed. It will usually take 6-7 working days. Kindly check back later."
            typing_effect(st, response)
            add_chat_session_details(st, response+"<br>")
            
            
            
            
            claim_form = user.claim_form.read()

            st.download_button(
                label="Previously uploaded claim form",
                data=claim_form,
                mime="application/pdf",
            )
            
            
            response= "Please tell me if my answer solved your query or if you need further support on any other policies."
            typing_effect(st, response)
            add_chat_session_details(st, response+"<br>")

            
             
    elif "policy" in prompt.lower():
        
        if not user.selected_policy_no:
            typing_effect(st, "Please select a policy number")
            add_chat_session_details(st, "Please select a policy number first. <br>")
            return "Please select a policy number first."  
        

        res1 = f"Here is the policy information for {prompt}."
        
        
        curr_policy = [policy for policy in user.policy_details if policy['Policy Number'] == user.selected_policy_no][0]
        
        policy_card =   f"""Your policy number is {curr_policy['Policy Number']} and your vehicle registration number is {curr_policy['Vehicle Registration Number']}."""
        
        res1 += policy_card
        
        
        info = "\nPlease tell me if my answer solved your query or if you need further support on any other policies."
        
        res1 += info
        
        typing_effect(st, res1)
        add_chat_session_details(st, res1)
    
    elif "form" in prompt.lower() and "claim" in prompt.lower():
        if not user.selected_policy_no:
            typing_effect(st, "Please select a policy number")
            add_chat_session_details(st, "Please select a policy number first. <br>")
            return "Please select a policy number first."  
        
        # upload claim form here
        res1 = "Please upload the claim form here."
        typing_effect(st, res1)
        add_chat_session_details(st, res1)
        
        st.session_state.claim_form_enabled = True   
        
    elif "thank" in prompt.lower():
        res1 = "Thank you for using ClaimX support. Please share the feedback and rate you experience…"
        
        typing_effect(st, res1)
        add_chat_session_details(st, res1+"<br>")     
        
        res1 = "Goodbye. Kindly comeback for future queries, we are always happy to help."
        
        typing_effect(st, res1)
        add_chat_session_details(st, res1+"<br>")
        st.session_state.user = User(name="User",age=0)
        
        
        
    else:
        res1 = "Sorry, I did not understand that. Please try again."
        typing_effect(st, res1)
        add_chat_session_details(st, res1+"<br>")
    
    