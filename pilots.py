import streamlit as st
from streamlit.components.v1 import html
import requests
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
        



        # Define custom configuration for the new agent
        API_KEY = st.secrets["elevenlabs_api_key"]
        CREATE_AGENT_URL = "https://api.elevenlabs.io/v1/convai/agents/create"

        headers = {
            "xi-api-key": API_KEY,
            "Content-Type": "application/json"
        }

        # Define custom configuration for the new agent
        payload = {
            "conversation_config": {
                "agent": {
                    "prompt": {
                        "prompt": "You are a 45-year-old female with chest pain for 3 hours."
                    },
                    "first_message": "I don't feel well, can you please help me?",
                    "language": "en"  # Use 'en' for English
                },
                "tts": {
                    "voice_id": "iP95p4xoKVk53GoZ742B",
                    "model_id": "eleven_turbo_v2"
                },
                "conversation": {
                    "max_duration_seconds": 300  # Example: 5-minute conversation
                }
            },
            "name": "TemporaryAgent"  # Optional: Name the agent for easy identification
        }

        # Make the API request to create the agent
        response = requests.post(CREATE_AGENT_URL, json=payload, headers=headers)

        if response.status_code == 200:
            agent_data = response.json()
            agent_id = agent_data["agent_id"]
            st.success(f"Temporary agent created: {agent_id}")
        else:
            st.error(f"Failed to create agent: {response.status_code} - {response.text}")

        widget_js = f"""
            <elevenlabs-convai agent-id="{agent_id}"></elevenlabs-convai>
            <script src="https://elevenlabs.io/convai-widget/index.js" async type="text/javascript"></script>
            """
        html(widget_js)