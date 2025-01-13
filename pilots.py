import streamlit as st
from streamlit.components.v1 import html

import streamlit as st

import streamlit as st

def check_password():
    """Returns `True` if the user has entered the correct password."""
    
    def validate_password():
        """Validates the entered password against the secret."""
        password_input = st.session_state.get("password", "")
        if password_input == st.secrets["password"]:
            st.session_state["password_correct"] = True
        else:
            st.session_state["password_correct"] = False
            # Increment attempt count
            st.session_state["login_attempts"] += 1

    # Initialize session state variables if not already set
    if "password_correct" not in st.session_state:
        st.session_state["password_correct"] = False
    if "login_attempts" not in st.session_state:
        st.session_state["login_attempts"] = 0
    if "first_load" not in st.session_state:
        st.session_state["first_load"] = True

    # Show instructions on the first load
    if st.session_state["first_load"]:
        st.write("Welcome! Please enter your password to continue.")
        st.session_state["first_load"] = False

    # Show the password input field if the password is incorrect or not entered
    if not st.session_state["password_correct"]:
        st.text_input(
            "Password",
            type="password",
            on_change=validate_password,
            key="password",
            placeholder="Enter your password"
        )
        
        # Show error message only after an incorrect attempt
        if st.session_state["login_attempts"] > 0 and not st.session_state["password_correct"]:
            st.error(f"😕 Password incorrect. Please try again. Attempts: {st.session_state['login_attempts']}")
        
        st.write("*Please contact David Liebovitz, MD if you need an updated password for access.*")
        return False

    # Password is correct
    st.success("✅ Password correct! Access granted.")
    return True


if check_password():
    
    with st.container(): 

        my_js_gpt = f"""
        <elevenlabs-convai agent-id="{st.secrets['agent_id']}"></elevenlabs-convai><script src="https://elevenlabs.io/convai-widget/index.js" async type="text/javascript"></script>
        """
        html(my_js_gpt)