
"""
No.4 Adding Basic Authentication

Objective: Secure a Streamlit app with simple username and password authentication.
Task: Implement a login page that requires a username and password to access the main app content.
Expected Output: The main app content is only accessible after successful login.
"""


from auth import require_auth
import streamlit as st


require_auth()
st.title("Protected Content")
st.write("This content is only visible after login.")
