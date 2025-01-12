import streamlit as st
from streamlit.components.v1 import html

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

    # Check if the password state exists, initialize it otherwise.
    if "password_correct" not in st.session_state:
        st.session_state["password_correct"] = False

    # Show the password input field if the password is incorrect or not entered.
    if not st.session_state["password_correct"]:
        st.text_input(
            "Password",
            type="password",
            on_change=validate_password,
            key="password",
            placeholder="Enter your password"
        )
        if "password" in st.session_state and not st.session_state["password_correct"]:
            st.error("😕 Password incorrect. Please try again.")
        st.write("*Please contact David Liebovitz, MD if you need an updated password for access.*")
        return False

    # Password is correct.
    return True

if check_password():

    my_js_gpt = """
    <elevenlabs-convai agent-id="leimLLc4N1UIKJ5640rU"></elevenlabs-convai><script src="https://elevenlabs.io/convai-widget/index.js" async type="text/javascript"></script>
    """
    html(my_js_gpt)