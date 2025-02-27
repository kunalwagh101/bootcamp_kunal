
# Persistent Queue System

## Approch

- **Producer:** Generates and submits jobs (random files) every 5 seconds.
- **Consumer:** Polls and processes jobs (by adding timestamps to file contents) and updates their status.
- **Admin:** A CLI tool (built with Typer) for listing, resubmitting, or marking jobs as failed.
- **Ops Dashboard:** A Streamlit app that displays current job statuses and details.

The system is designed to be robust and fault-tolerant by using SQLite transactions for atomic operations and Supervisor to manage processes.

## System Design & Architecture
- **PersistentQInterface:** An abstract base class defining the API for enqueuing, dequeuing, updating, and listing jobs.
- **PersistentQSQLAlchemy:** A concrete implementation using SQLAlchemy for ORM-based access to an SQLite database. It leverages SQLite transactions to ensure that jobs are processed atomically.
- **Modules:**
  - **Producer:** Generates random files and enqueues them.
  - **Consumer:** Dequeues jobs, processes them by prepending timestamps, and updates job status.
  - **Admin:** Provides CLI commands to manage jobs.
  - **Ops:** A Streamlit dashboard for real-time monitoring.
- **Process Management:** Uses Supervisor (or an alternative on Windows, such as Honcho or WSL) to manage the producer and consumer processes.



## Activate the Virtual Environment:

- **for linux use**

```
python -m venv venv
source venv/bin/activate
```
- **or use poetry**

```
poetry install
poetry run typer
```



## Install Dependencies 

```
pip install -r requirements.txt
```


## Running the Application


### 1. Running Producer and Consumer with Supervisor

- **Note: Supervisor is Unix-based. Windows users may need to use WSL or an alternative like Honcho.**

- **Supervisor Configuration: The configuration file is located at supervisor/supervisord.conf.**

### Start Supervisor:

- **this will launch 3 consumers at a time**
```


```

- **To monitor consumer processes run this**
```
poetry run python -m consumer.consumer

```

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

- **Mark a Job as Failed**

```
poetry run python -m admin.admin mark-failed <job_id>   

``` 
- **check all the failed jobs**
```
poetry run python -m admin.admin failedjobs
```


- **check status with**

```
supervisorctl status
```
- **or use**

```
 supervisorctl -c supervisor/supervisord.conf status
```


- **Create multiple consumers !  --count  1 =  adds 3 new consumers**

```
poetry run python -m manager.consumer_manager --count 1
```

- **kill a consumer_<consumer id>** 


```
supervisorctl stop consumer_00
```

- **or try**
```
supervisorctl -c supervisor/supervisord.conf stop consumer:consumer_00

```


- **Run this to monitor all process at once**
```
poetry run python -m admin.admin monitor

```


- **To delete all the jobs files created locally 'RUN'**
```
poetry run python -m admin.admin delete-job-files --directory .
```

- **To delete all the jobs from database 'RUN'**

```
poetry run python -m admin.admin delete-db-jobs
```


- **To manually assign (or reassign) a job file to a chosen consumer**


```
poetry run python -m admin.admin assign-job <job_id> <consumer_id>

```