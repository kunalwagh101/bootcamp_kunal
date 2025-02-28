# Persistent Queue System

A robust and fault-tolerant job queue system that leverages SQLite transactions and Supervisor for process management. This system comprises producers, consumers, an admin CLI, and an ops dashboard for real-time monitoring.

---

## Table of Contents

- [Overview](#overview)
- [Approach](#approach)
- [System Design & Architecture](#system-design--architecture)
- [Setup Instructions](#setup-instructions)
  - [Activate the Virtual Environment](#activate-the-virtual-environment)
  - [Install Dependencies](#install-dependencies)
- [Running the Application](#running-the-application)
  - [1. Running Producer and Consumer with Supervisor](#1-running-producer-and-consumer-with-supervisor)
  - [2. Running the Ops Dashboard (Streamlit)](#2-running-the-ops-dashboard-streamlit)
  - [3. Using the Admin CLI](#3-using-the-admin-cli)
- [Additional Commands](#additional-commands)
- [Notes](#notes)

---

## Overview

This project implements a persistent queue system with the following key components:

- **Producer:** Generates and submits jobs (random files) every 5 seconds.
- **Consumer:** Polls and processes jobs by prepending timestamps to file contents and updating their status.
- **Admin:** A CLI tool (built with Typer) for listing, resubmitting, or marking jobs as failed.
- **Ops Dashboard:** A Streamlit app that displays current job statuses and details.

The system is designed for robustness and fault tolerance using SQLite transactions for atomic operations and Supervisor for process management.

---

## Approach

- **Producer:** Periodically generates random file jobs and enqueues them.
- **Consumer:** Continuously polls the queue, processes each job (by adding timestamps), and updates the job status.
- **Admin:** Offers CLI commands to manage the queue, such as listing jobs, resubmitting failed jobs, and marking jobs as failed.
- **Ops Dashboard:** Provides real-time monitoring via an interactive Streamlit interface.
- **Process Management:** Utilizes Supervisor (or alternatives like Honcho/WSL on Windows) to manage and monitor producer and consumer processes.

---

## System Design & Architecture

- **PersistentQInterface:** An abstract base class that defines the API for job operations such as enqueuing, dequeuing, updating, and listing jobs.
- **PersistentQSQLAlchemy:** A concrete implementation using SQLAlchemy for ORM-based access to an SQLite database, ensuring atomic job processing.
- **Modules:**
  - **Producer:** Generates random files and enqueues them.
  - **Consumer:** Dequeues jobs, processes them (by prepending timestamps), and updates their status.
  - **Admin:** Provides CLI commands for managing jobs.
  - **Ops:** A Streamlit dashboard for real-time monitoring.
- **Process Management:** Uses Supervisor (or Windows alternatives) to manage the lifecycle of producer and consumer processes.

---

## Setup Instructions

### Activate the Virtual Environment

#### For Linux:

```bash
python -m venv venv
source venv/bin/activate
Or use Poetry:
bash
Copy
Edit
poetry install
poetry run typer
Install Dependencies
bash
Copy
Edit
pip install -r requirements.txt
Running the Application
1. Running Producer and Consumer with Supervisor
Note: Supervisor is Unix-based. Windows users may need to use WSL or an alternative like Honcho.

Supervisor Configuration:
The configuration file is located at supervisor/supervisord.conf.

Start Supervisor:

bash
Copy
Edit
supervisord -c supervisor/supervisord.conf
Monitor Consumer Processes:

bash
Copy
Edit
poetry run python -m consumer.consumer
2. Running the Ops Dashboard (Streamlit)
Start the Dashboard:

bash
Copy
Edit
poetry run streamlit run ops/ops.py
Open your Browser at:
http://localhost:8501

3. Using the Admin CLI
The Admin module, built with Typer, provides several commands for managing jobs.

List All Jobs:

bash
Copy
Edit
poetry run python -m admin.admin list-jobs
Resubmit a Job:

bash
Copy
Edit
poetry run python -m admin.admin resubmit <job_id>
Mark a Job as Failed:

bash
Copy
Edit
poetry run python -m admin.admin mark-failed <job_id>
Check All Failed Jobs:

bash
Copy
Edit
poetry run python -m admin.admin failedjobs
Additional Commands
Check Process Status with Supervisor:

bash
Copy
Edit
supervisorctl status
Or

bash
Copy
Edit
supervisorctl -c supervisor/supervisord.conf status
Create Multiple Consumers:
(Note: --count 1 adds 3 new consumers)

bash
Copy
Edit
poetry run python -m manager.consumer_manager --count 1
Stop a Specific Consumer:

bash
Copy
Edit
supervisorctl stop consumer_00
Or

bash
Copy
Edit
supervisorctl -c supervisor/supervisord.conf stop consumer:consumer_00
Monitor All Processes:

bash
Copy
Edit
poetry run python -m admin.admin monitor
Delete All Job Files:

bash
Copy
Edit
poetry run python -m admin.admin delete-job-files --directory .
Delete All Jobs from the Database:

bash
Copy
Edit
poetry run python -m admin.admin delete-db-jobs
Manually Assign (or Reassign) a Job to a Consumer:

bash
Copy
Edit
poetry run python -m admin.admin assign-job <job_id> <consumer_id>