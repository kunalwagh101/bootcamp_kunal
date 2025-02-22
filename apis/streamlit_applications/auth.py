"""
No.4 Adding Basic Authentication

Objective: Secure a Streamlit app with simple username and password authentication.
Task: Implement a login page that requires a username and password to access the main app content.
Expected Output: The main app content is only accessible after successful login.
"""


import streamlit as st

def login():
    st.session_state["authenticated"] = False
    username = st.text_input("Username", key="username")
    password = st.text_input("Password", type="password", key="password")
    if st.button("Login"):
        if username == "admin" and password == "password":
            st.session_state["authenticated"] = True
            st.success("Login successful!")
        else:
            st.error("Invalid credentials")

def require_auth():
    if "authenticated" not in st.session_state or not st.session_state["authenticated"]:
        login()
        st.stop()
