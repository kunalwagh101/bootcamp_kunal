import streamlit as st
from persistent.persistent import PersistentQSQLite


QUEUE = PersistentQSQLite()

st.title("Ops Dashboard - Persistent Queue System")
st.write("This dashboard shows the current status of all jobs.")

jobs = QUEUE.list_jobs()

if jobs:
    st.write("### Job List")
    for job in jobs:
        st.write(f"Job ID: {job[0]}, Status: {job[2]}")
else:
    st.write("No jobs found.")
