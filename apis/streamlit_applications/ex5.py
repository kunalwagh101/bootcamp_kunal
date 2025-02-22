"""
No.5 Implement Reactivity Using Widgets

Objective: Demonstrate Streamlit’s reactivity through interactive widgets.
Task: Create an app with a slider widget that dynamically updates a displayed number based on the slider’s position.
Expected Output: A web app with a slider that, when adjusted, updates a displayed value in real-time.e(f"Slider Value: {slider_value}")

"""


import streamlit as st

st.title("Interactive Slider")

slider_value = st.slider("Choose a number", 0, 100, 50)
st.write(f"Slider Value: {slider_value}")
