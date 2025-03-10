
import datetime
import pandas as pd
import streamlit as st
import sys
import sys
from pathlib import Path

current_dir = Path(__file__).resolve().parent
project_root = current_dir.parent
sys.path.append(str(project_root))
from persistent.persistentQSQLAlchemy import PersistentQSQLAlchemy as PersistentQ

QUEUE = PersistentQ()


st.set_page_config(page_title="Persistent Queue Dashboard", layout="wide")


st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Dashboard", "Manage Jobs", "Actions"])

if page == "Dashboard":
    st.title("Persistent Queue Dashboard")
    st.markdown("This dashboard shows the current status of all jobs in the persistent queue. The list automatically refreshes every 5 seconds.")
    
    
    jobs = QUEUE.list_jobs()  
    if jobs:
        df = pd.DataFrame(jobs, columns=["Job ID", "Job Data", "Status", "Consumer"])
        st.dataframe(df, use_container_width=True)
    else:
        st.info("No jobs found.")
    
    st.markdown("_(The page will auto-refresh every 5 seconds)_")
    st.experimental_set_query_params(refresh=str(datetime.datetime.now()))
    st.experimental_rerun()

elif page == "Manage Jobs":
    st.title("Manage Jobs")
    st.markdown("Use the form below to assign, resubmit, or mark a job as failed.")
    
    operation = st.selectbox("Select Operation", ["Assign Job", "Resubmit Job", "Mark as Failed"])
    job_id = st.text_input("Job ID", placeholder="Enter the job ID")
    
    if operation == "Assign Job":
        consumer_id = st.text_input("Consumer ID", placeholder="Enter consumer ID")
        if st.button("Assign Job"):
            if job_id and consumer_id:
                result = QUEUE.assign_job(job_id, consumer_id)
                if result:
                    st.success(f"Job {job_id} assigned to consumer {consumer_id}.")
                else:
                    st.error(f"Failed to assign job {job_id}.")
            else:
                st.error("Please provide both Job ID and Consumer ID.")
    
    elif operation == "Resubmit Job":
        if st.button("Resubmit Job"):
            if QUEUE.get_job_status(job_id) is None:
                st.error("Job not found.")
            else:
                QUEUE.update_job_status(job_id, "pending")
                st.success(f"Job {job_id} resubmitted.")
    
    elif operation == "Mark as Failed":
        if st.button("Mark Job as Failed"):
            QUEUE.update_job_status(job_id, "failed")
            st.success(f"Job {job_id} marked as failed.")
    
    st.markdown("---")
    st.subheader("Current Jobs")
    jobs = QUEUE.list_jobs()
    if jobs:
        df = pd.DataFrame(jobs, columns=["Job ID", "Job Data", "Status", "Consumer"])
        st.dataframe(df, use_container_width=True)
    else:
        st.info("No jobs found.")

elif page == "Actions":
    st.title("Actions")
    st.markdown("Perform bulk actions on jobs.")
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Delete All Job Records from Database"):
            if QUEUE.delete_all():
                st.success("All job records have been deleted.")
            else:
                st.error("Failed to delete job records.")
    
    with col2:
        directory = st.text_input("Directory for Job Files", value=".")
        if st.button("Delete All Job Files"):
            from pathlib import Path
            path = Path(directory)
            job_files = list(path.glob("job_*.txt"))
            if not job_files:
                st.info("No job files found.")
            else:
                errors = []
                for job_file in job_files:
                    try:
                        job_file.unlink()
                    except Exception as e:
                        errors.append(f"Error deleting {job_file}: {e}")
                if errors:
                    st.error("\n".join(errors))
                else:
                    st.success("All job files deleted.")
    
    st.markdown("---")
    st.subheader("Refresh Data")
    if st.button("Refresh Dashboard"):
        st.experimental_rerun()
