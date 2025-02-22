"""

No.2 Implementing Multipage App

Objective: Develop a multipage Streamlit app with navigation.
Task: Create a Streamlit app with two pages: Home and About. Each page should display a title indicating the page name.
Expected Output: A Streamlit app where users can navigate between Home and About pages.
"""



import streamlit as st

st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to",["home" ,"about"])

if page == "home":
    st.title("welcome home")

elif page == "about":
    st.title("welcome to about page")
    