
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




# STEPS TO RUN THE APPLICATION

# Clone the repository
```

git clone git@github.com:kunalwagh101/bootcamp_kunal.git

```


# Create a virtual environment

```

cd bootcamp_kunal

```

**For Linux and macOS**
   
```
python -m venv venv
source venv/bin/activate

```

**For Windows**
 
```
    pip install virtualenv
    python -m venv venv
    virtualenv venv
    venv/Scripts/activate

```

# Install the necessary modules

```

pip install -r requirements.txt

```

***Just in case some dependence might not get install so ran***

```
pip install pyyaml
pip install typer

```

**Just cd into the classes_and_object, data_structures, decorators_and_lambda and more_classes**


***And use this following command to run all of the python files in the specific folder***



 
```

python script.py

```

***or follow the readme.md in that particular folder***