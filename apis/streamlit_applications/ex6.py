
"""
No.6 Integration of Graphs with Matplotlib

Objective: Integrate a Matplotlib graph into a Streamlit app.
Task: Generate a simple line graph using Matplotlib based on a random dataset and display it in a Streamlit app.
Expected Output: A Streamlit app that shows a Matplotlib line graph.
"""


import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

st.title("Matplotlib Graph")

x = np.linspace(0, 10, 100)
y = np.sin(x)

fig, ax = plt.subplots()
ax.plot(x, y)

st.pyplot(fig)
