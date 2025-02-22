"""
NO.7 Interactive Data Tables with Pandas

Objective: Display interactive data tables using Pandas DataFrame.
Task: Load a dataset into a Pandas DataFrame and use Streamlit to display the table interactively.
Expected Output: A Streamlit app with an interactive table based on the loaded dataset.
"""

import pandas as pd
import streamlit as st


st.title("Data Table")

df = pd.DataFrame({
    "Name": ["Alice", "Bob", "Charlie"],
    "Age": [25, 30, 35],
    "Score": [85, 90, 78]
})

st.dataframe(df)
