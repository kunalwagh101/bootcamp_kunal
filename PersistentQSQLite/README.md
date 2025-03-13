# Persistent Queue System 🚀

A robust, fault-tolerant system for managing persistent queues with Producers, Consumers, an Admin CLI, and an Ops Dashboard.

---

## Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Setup & Installation](#setup--installation)
- [Running the Application](#running-the-application)
  - [1. Running Producer and Consumer with Supervisor](#1-running-producer-and-consumer-with-supervisor)
  - [2. Running the Ops Dashboard (Streamlit)](#2-running-the-ops-dashboard-streamlit)
  - [3. Using the Admin CLI](#3-using-the-admin-cli)
- [Additional Commands](#additional-commands)
- [Notes](#notes)

---

## Overview

- **Producer:** Generates and submits jobs (random files) every 5 seconds.
- **Consumer:** Polls and processes jobs (by adding timestamps to file contents) and updates their status.
- **Admin:** A CLI tool (built with [Typer](https://typer.tiangolo.com/)) for listing, resubmitting, or marking jobs as failed.
- **Ops Dashboard:** A [Streamlit](https://streamlit.io/) app that displays current job statuses and details.

The system leverages SQLite transactions for atomic operations and uses Supervisor to manage processes, ensuring high reliability and fault tolerance.

---

## Architecture

### Core Components

- **PersistentQInterface:**  
  An abstract base class defining the API for enqueuing, dequeuing, updating, and listing jobs.

- **PersistentQSQLAlchemy:**  
  A concrete implementation using SQLAlchemy for ORM-based access to an SQLite database. It leverages SQLite transactions to ensure atomic job processing.

### Modules

- **Producer:**  
  Generates random files and enqueues them.

- **Consumer:**  
  Dequeues jobs, processes them (by prepending timestamps), and updates their status.

- **Admin:**  
  Provides CLI commands to manage jobs.

- **Ops:**  
  A Streamlit dashboard for real-time monitoring of job statuses.

### Process Management

- **Supervisor:**  
  Used to manage the producer and consumer processes.  
  *(Note: For Windows users, consider using WSL or an alternative like [Honcho](https://github.com/nickstenning/honcho).)*

---

## Setup & Installation

### 1. Activate the Virtual Environment

- **For Linux:**
  ```bash
  python -m venv venv
  source venv/bin/activate
  ```

- **Or Using Poetry:**
  ```bash
  poetry install
  poetry run typer
  ```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

- **Environment Configuration**

  Create a `.env` file in the project root with the following content:

  ```ini
    QUEUE_DB_FILE=queue.db
    MAX_ATTEMPTS=3
    TIMEOUT_SECONDS=60
    INTERVAL_TIME = 5

  ```

---

## Running the Application

### 1. Running Producer and Consumer with Supervisor

> **Note:** Supervisor is Unix-based. Windows users may need to use WSL or an alternative like Honcho.

- **Supervisor Configuration:**  
  The configuration file is located at `supervisor/supervisord.conf`.

#### Start Supervisor:
```bash
supervisord -c supervisor/supervisord.conf
```

#### Monitor All Processes:
```bash
poetry run python -m admin.admin monitor-activity --interval 5

```

#### Launch the Interactive Manager:
```bash
poetry run python -m manager.manager
```

---

### 2. Running the Ops Dashboard (Streamlit)

Launch the interactive dashboard:
```bash
poetry run streamlit run ops/ops.py
```
Then open your browser at [http://localhost:8501](http://localhost:8501) to view the dashboard.

---

### 3. Using the Admin CLI

The Admin module is built with Typer for managing jobs. Example commands include:

#### List All Jobs:
```bash
poetry run python -m admin.admin list-jobs
```

#### Resubmit a Job:
```bash
poetry run python -m admin.admin resubmit <job_id>
```

#### Mark a Job as Failed:
```bash
poetry run python -m admin.admin mark-failed <job_id>
```

#### Check All Failed Jobs:
```bash
poetry run python -m admin.admin failedjobs
```

#### Check Supervisor Status:
```bash
supervisorctl -c supervisor/supervisord.conf status
```
*Or simply:*
```bash
supervisorctl status
```

---

## Additional Commands


#### Kill a Consumer  
Replace `<consumer_id>` as needed:
```bash
supervisorctl -c supervisor/supervisord.conf stop consumer:consumer_00
```
*Or:*
```bash
supervisorctl stop consumer_00
```

#### Monitor All Processes
```bash
poetry run python -m admin.admin monitor
```

#### Delete All Local Job Files
```bash
poetry run python -m admin.admin delete-job-files --directory .
```

#### Delete All Jobs from the Database
```bash
poetry run python -m admin.admin delete-db-jobs
```

#### Manually Assign (or Reassign) a Job to a Consumer
```bash
poetry run python -m admin.admin assign-job <job_id> <consumer_id>
```

---

## Notes

- **Virtual Environment:** Ensure the virtual environment is activated before running any commands.
- **Supervisor Alternatives:** Windows users can use [WSL](https://docs.microsoft.com/en-us/windows/wsl/) or [Honcho](https://github.com/nickstenning/honcho) for process management.
- **Interactive Monitoring:** Use the Ops Dashboard for real-time insights into job statuses.

