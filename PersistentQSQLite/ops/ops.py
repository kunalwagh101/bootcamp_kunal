import streamlit as st
from persistent import get_queue

QUEUE = get_queue()

st.title("Ops Dashboard - Persistent Queue System")
st.write("Current job statuses:")

jobs = QUEUE.list_jobs()

if jobs:
    for job in jobs:
        st.write(f"Job ID: {job[0]}, Status: {job[2]}")
else:
    st.write("No jobs found.")
