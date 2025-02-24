# Persistent Queue System

## Overview
A multi-application system that implements a persistent queue using SQLite and SQLAlchemy. The system includes:
- **Producer:** Generates and submits jobs (random files).
- **Consumer:** Processes jobs by adding timestamps.
- **Admin:** CLI tool to manage jobs.
- **Ops Dashboard:** Streamlit app for monitoring job statuses.


## Activate the Virtual Environment:

- **for linux use**

```
python -m venv venvv
source venvv/bin/activate
```
- **or use poetry**

```
poetry install
poetry run typer


```

'''
pip install requirements.txt
'''

## Install Dependencies 

```
pip install requirements.txt

```


## Running the Application


### 1. Running Producer and Consumer with Supervisor

- **Note: Supervisor is Unix-based. Windows users may need to use WSL or an alternative like Honcho.**

- **Supervisor Configuration: The configuration file is located at supervisor/supervisord.conf.**

### Start Supervisor:

```
supervisord -c supervisor/supervisord.conf
```

- **Verify Processes:**



### 2. Running the Ops Dashboard (Streamlit)

- **To run the interactive dashboard:**

```
poetry run streamlit run ops/ops.py
```

- **Then, open your browser at http://localhost:8501 to view the dashboard**

### 3. Using the Admin CLI
- **The Admin module is built with Typer to manage jobs. Example commands include:**

- **List All Jobs:**

```
poetry run python -m admin.admin list-jobs

```

### Resubmit a Job:

```
poetry run python -m admin.admin resubmit <job_id>
```

-**Mark a Job as Failed**

```
poetry run python -m admin.admin mark-failed <job_id>   

``` 