"""
No.8 Using Plotly for Advanced Graphs

Objective: Create advanced interactive graphs with Plotly in Streamlit.
Task: Embed a Plotly graph (e.g., a scatter plot) in a Streamlit app, using a random or predefined dataset.
Expected Output: A Streamlit app displaying an interactive Plotly scatter plot.
"""

import plotly.express as px
import streamlit as st
import pandas as pd
import numpy as np

st.title("Plotly Scatter Plot")

df = pd.DataFrame({
    "x": np.random.rand(50),
    "y": np.random.rand(50),
    "category": np.random.choice(["A", "B", "C"], 50)
})

fig = px.scatter(df, x="x", y="y", color="category")
st.plotly_chart(fig)
