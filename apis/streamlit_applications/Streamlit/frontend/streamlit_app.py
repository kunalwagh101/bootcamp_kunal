

import streamlit as st
import requests
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px


def local_css(file_name):
    try:
        with open(file_name) as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    except Exception as e:
        st.error("Error loading CSS file: " + str(e))


local_css("static/custom.css")

def login_page():
    st.title("Login")
    st.write("Please log in to access the application.")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        try:
          
            response = requests.post("http://localhost:8000/login", json={
                "username": username,
                "password": password
            })
            if response.status_code == 200:
                st.session_state["authenticated"] = True
                st.session_state["username"] = username
                st.success("Login successful!")
            else:
                st.error("Invalid credentials. Please try again.")
        except Exception as e:
            st.error("Error connecting to the backend: " + str(e))


def home_page():
    st.header("Hello, Streamlit!")
    st.write("Welcome to the Home Page of this integrated FastAPI & Streamlit app.")


def about_page():
    st.header("About")
    st.write(
        "This multipage application demonstrates a full-stack integration using FastAPI (with SQLite for authentication) "
        "and a Streamlit frontend. It features interactive widgets, data visualizations, and session state management."
    )


def counter_page():
    st.header("Counter App")
    if "count" not in st.session_state:
        st.session_state["count"] = 0
    if st.button("Increment"):
        st.session_state["count"] += 1
    st.write(f"Current count: {st.session_state['count']}")


def slider_page():
    st.header("Slider Widget")
    slider_value = st.slider("Adjust the slider", 0, 100, 50)
    st.write(f"Slider value: {slider_value}")


def matplotlib_page():
    st.header("Matplotlib Graph")
   
    x = np.linspace(0, 10, 100)
    y = np.sin(x) + np.random.normal(0, 0.1, size=x.shape)
    fig, ax = plt.subplots()
    ax.plot(x, y, label="Random Data")
    ax.set_title("Matplotlib Line Graph")
    ax.set_xlabel("X-axis")
    ax.set_ylabel("Y-axis")
    ax.legend()
    st.pyplot(fig)


def data_table_page():
    st.header("Interactive Data Table")
 
    df = pd.DataFrame({
        "Column 1": np.random.randint(0, 100, 10),
        "Column 2": np.random.randint(0, 100, 10),
        "Column 3": np.random.randint(0, 100, 10)
    })
    st.dataframe(df)


def plotly_page():
    st.header("Plotly Scatter Plot")

    df = pd.DataFrame({
        "x": np.random.rand(100),
        "y": np.random.rand(100),
        "Category": np.random.choice(["A", "B", "C"], 100)
    })
    fig = px.scatter(df, x="x", y="y", color="Category", title="Interactive Plotly Scatter Plot")
    st.plotly_chart(fig)


def main():
    if "authenticated" not in st.session_state or not st.session_state["authenticated"]:
        login_page()
    else:
      
        st.sidebar.title("Navigation")
        page = st.sidebar.radio("Go to", [
            "Home", 
            "About", 
            "Counter", 
            "Slider", 
            "Matplotlib Graph", 
            "Data Table", 
            "Plotly Graph"
        ])
        
        if page == "Home":
            home_page()
        elif page == "About":
            about_page()
        elif page == "Counter":
            counter_page()
        elif page == "Slider":
            slider_page()
        elif page == "Matplotlib Graph":
            matplotlib_page()
        elif page == "Data Table":
            data_table_page()
        elif page == "Plotly Graph":
            plotly_page()

        if st.sidebar.button("Logout"):
            st.session_state.clear()
            st.experimental_rerun()

if __name__ == '__main__':
    main()
