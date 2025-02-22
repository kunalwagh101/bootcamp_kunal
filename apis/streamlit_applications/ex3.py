"""
No.3 
State Management with Session State

Objective: Utilize Streamlit’s session state for state management.
Task: Build a counter app that increments a number each time a button is pressed, using Streamlit's session state to keep track of the count.
Expected Output: A web app with a button that, when clicked, increments and displays a counter.

"""

import streamlit as st

st.title("Counter App")

if "count" not in st.session_state:
    st.session_state.count = 0

if st.button("Increment"):
    st.session_state.count += 1

st.write(f"Count: {st.session_state.count}")
