
# Persistent Queue System 🚀

A robust, fault-tolerant system for managing persistent queues with multiple Producers, Consumers, an Admin CLI, an Interactive Manager (TUI), and an Ops Dashboard (Streamlit). This document serves as a roadmap and design guide for anyone who wishes to use or contribute to the project.

---

## Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
  - [Core Components](#core-components)
  - [Flow Diagram](#flow-diagram)
  - [Sequence Diagram](#sequence-diagram)
  - [Process Management Diagram](#process-management-diagram)
- [Design Information](#design-information)
- [Design Decisions & Q&A](#design-decisions--qa)
  - [Atomic Status Updates](#atomic-status-updates)
  - [Job Filtering](#job-filtering)
  - [Environment Configuration](#environment-configuration)
  - [SQLAlchemy vs. Raw SQL](#sqlalchemy-vs-raw-sql)
  - [Commented-Out Code & Code Duplication](#commented-out-code--code-duplication)
  - [Consumer ID Usage](#consumer-id-usage)
  - [Producer Improvements](#producer-improvements)
  - [Consumer Failure Handling](#consumer-failure-handling)
  - [CLI vs. Web-Based Interfaces](#cli-vs-web-based-interfaces)
  - [Periodic Cleanup](#periodic-cleanup)
- [Setup & Installation](#setup--installation)
- [Running the Application](#running-the-application)
  - [Supervisor Process Management](#supervisor-process-management)
  - [Ops Dashboard (Streamlit)](#ops-dashboard-streamlit)
  - [Admin CLI](#admin-cli)
  - [Interactive Manager (TUI)](#interactive-manager-tui)
- [Additional Commands](#additional-commands)
- [Additional Notes](#additional-notes)
- [Usage Instructions](#usage-instructions)

---

## Overview

- **Producer:** Generates and submits jobs (temporary files with random content) every 5 seconds.
- **Consumer:** Atomically dequeues and processes jobs (e.g., by appending timestamps to file contents) and updates their status. An attempt counter marks jobs as "failed" after repeated errors.
- **Admin CLI:** A Typer-based command-line tool for listing jobs, resubmitting jobs, marking them as failed, deleting job records, and assigning/reassigning jobs.
- **Interactive Manager (TUI):** A prompt_toolkit-based interactive interface for real-time administration and monitoring.
- **Ops Dashboard:** A Streamlit app that displays current job statuses and details.
- **Supervisor:** Manages Producer and Consumer processes, ensuring they auto-restart if they crash.

---

## Architecture

### Core Components

- **PersistentQInterface:**  
  An abstract interface defining the API for enqueuing, dequeuing, updating status, listing jobs, and job assignment.

- **PersistentQSQLAlchemy:**  
  A concrete implementation using SQLAlchemy for ORM-based access to an SQLite database. It leverages environment-based configuration and timezone-aware datetime objects to ensure atomic operations and internal filtering. This design allows future flexibility to swap out SQLite for another backend.

### Flow Diagram

~~~mermaid
flowchart TB;
    Producer(Producer) --> EnqueueJob[Enqueue Job];
    EnqueueJob --> PersistentQueue[Persistent Queue];
    PersistentQueue --> DequeueJob[Dequeue Job];
    DequeueJob --> Consumer(Consumer);
    Consumer --> ProcessJob[Process Job];
    ProcessJob --> MarkDone[Mark as Done];
    ProcessJob --> MarkFailed[Mark as Failed];
    PersistentQueue --> ResubmitJob[Resubmit Job];
    PersistentQueue --> CancelJob[Cancel Job];
    ResubmitJob --> PersistentQueue;
    CancelJob --> PersistentQueue;
    MarkFailed --> PersistentQueue;
~~~

### Sequence Diagram

~~~mermaid
sequenceDiagram
    participant P as Producer
    participant Q as Persistent Queue
    participant C as Consumer
    participant A as Admin/Ops

    P->>Q: Enqueue Job
    Q->>C: Dequeue Job
    C->>Q: Process Job and Update Status
    A->>Q: Resubmit/Cancel Job (if needed)
~~~

### Process Management Diagram

~~~mermaid
flowchart LR;
    Supervisor --> Producer;
    Supervisor --> Consumer;
    Manager --- Ops;
    Producer --> PersistentQueue;
    Consumer --> PersistentQueue;
~~~

---

## Design Information

- We chose **SQLAlchemy** as our ORM to reduce boilerplate and allow flexibility for future database swaps.
- **Supervisor** is used to ensure high availability by automatically restarting Producers and Consumers if they crash.
- The **.env** configuration approach was adopted for ease of deployment across multiple environments.
- **Decoupling** the job production and consumption processes facilitates asynchronous processing and improves scalability.
- Both **CLI and TUI interfaces** were implemented to cater to different user preferences, providing both quick command-line operations and a rich interactive experience.
- **Streamlit** was selected for the Ops Dashboard to offer an intuitive, web-based monitoring solution.

---

## Design Decisions & Q&A

### Atomic Status Updates

**Q:** How are job status updates handled atomically?  
**A:** The system uses SQLAlchemy sessions and transactions to update a job’s status in one commit, preventing race conditions.

### Job Filtering

**Q:** Why is job filtering handled internally by the system?  
**A:** Methods like `get_pending_jobs()` reduce data transfer by performing filtering directly in the database query, leveraging built-in database efficiencies.

### Environment Configuration

**Q:** Why use environment variables instead of hardcoded values?  
**A:** Environment configuration via a `.env` file increases flexibility and allows for different setups without changing the code.

### SQLAlchemy vs. Raw SQL

**Q:** Why opt for SQLAlchemy instead of raw SQL?  
**A:** SQLAlchemy reduces boilerplate code, minimizes errors, and abstracts database interactions, making future migrations easier.

### Commented-Out Code & Code Duplication

**Q:** How is code duplication handled?  
**A:** Common operations, such as session handling, are encapsulated in helper methods. Any obsolete commented code has been removed for clarity.

### Consumer ID Usage

**Q:** How is the consumer ID used in job processing?  
**A:** Each consumer gets a unique ID when processing a job. This ensures that only one consumer handles a job, and if a consumer crashes, the job can be re-assigned.

### Producer Improvements

**Q:** How does the producer simulate job generation?  
**A:** It uses Python’s `tempfile` module to create unique temporary files with random content, mimicking realistic job submissions.


### CLI vs. Web-Based Interfaces

**Q:** Why offer both CLI and web-based interfaces?  
**A:** A CLI is great for quick, single-user operations, but a TUI and web dashboard provide richer, concurrent management capabilities for multiple administrators.

### Periodic Cleanup

**Q:** Who handles periodic cleanup of stuck jobs?  
**A:** Cleanup is triggered at the start of each `dequeue()` operation, with potential for scheduling as a background job in production.


### Consumers

**Q:** what happens to the process when all the consumers dies ?  
**A:** 1. If Supervisor is configured properly, it will automatically restart the consumer processes. This means that even if all consumers crash, Supervisor should bring them back up so processing can resume.    
       2. Any jobs that were "processing" when the consumers died remain in the database if a job exceeds `MAX_ATTEMPTS`, it is marked as "failed. When a new consumer starts up, it will trigger the cleanup logic
     

**Q:** How can i add more consumers ?   
**A:** Refer to - [Add More Consumers](#add-more-consumers)  
    

**Q:** How can i Kill a consumer ?   
**A:**   supervisorctl -c supervisor/supervisord.conf stop consumer:<consumer_id>
```bash
 supervisorctl -c supervisor/supervisord.conf stop consumer:consumer_00
```
    




---

## Setup & Installation

1. **Virtual Environment**

   **For Linux/WSL:**

   ~~~bash
   python -m venv venv
   source venv/bin/activate
   ~~~

   **Using Poetry:**

   ~~~bash
   poetry install
   ~~~
## Setup & Installation

  2. **Environment Configuration**

  Create a `.env` file in the project root with the following content:

  ```ini
    QUEUE_DB_FILE=queue.db
    MAX_ATTEMPTS=3
    TIMEOUT_SECONDS=60
    INTERVAL_TIME = 5
  
  ```

  **Add More Consumers**



  ```ini

    [program:consumer]
    command=poetry run python -m consumer.consumer
    numprocs= 1 #Change this number to the desired number of consumers
    process_name=%(program_name)s_%(process_num)02d
    autostart=true
    autorestart=true
    stdout_logfile=consumer.log
    stderr_logfile=consumer_err.log
  ```

  **Explanation:**

  - **`numprocs=3`**:  In this example, we've changed `numprocs` to `3`. This tells Supervisor to start and manage **three** consumer processes. You can change `3` to any number of consumers you need.
  - **`process_name=%(program_name)s_%(process_num)02d`**: This line ensures that each consumer process will have a unique name (e.g., `consumer_00`, `consumer_01`, `consumer_02`, etc.), which is helpful for monitoring and managing them individually using `supervisorctl`.


  

**After making these changes:**

1.  **Save** the `supervisor/supervisord.conf` file.
2.  **Restart Supervisor** to apply the new configuration:

    ~~~bash
    supervisorctl reread
    supervisorctl update
    ~~~

3.  **Check the status** of your processes to confirm the new consumers are running:

    ~~~bash
    supervisorctl status consumer*
    ~~~

You should now see the increased number of consumer processes listed in the status output. Each consumer will independently dequeue and process jobs from the queue, increasing the system's processing capacity.

3. **Install Dependencies**

   Ensure all required packages are installed via Poetry:

   ~~~bash
   poetry install
   ~~~

---

## Running the Application

### Supervisor Process Management

**Start Supervisor:**

~~~bash
supervisord -c supervisor/supervisord.conf
~~~

**Check Process Status:**

~~~bash
supervisorctl status
~~~


**monitor all activities:**

~~~bash
poetry run python -m admin.admin monitor-activity --interval 5
~~~


### Interactive Manager (TUI)

**Launch the Interactive Manager:**

~~~bash
poetry run python -m manager.manager
~~~



### Ops Dashboard (Streamlit)

**Run the Dashboard:**

~~~bash
poetry run streamlit run ops/ops.py
~~~

Access the Dashboard at `http://localhost:8501`.

### Admin CLI

**List All Jobs:**

~~~bash
poetry run python -m admin.admin list-jobs
~~~

**Resubmit a Job:**

~~~bash
poetry run python -m admin.admin resubmit <job_id>
~~~

**Mark a Job as Failed:**

~~~bash
poetry run python -m admin.admin mark-failed <job_id>
~~~

**Delete All Job Records:**

~~~bash
poetry run python -m admin.admin delete-db-jobs
~~~

**Delete All Job Files:**

~~~bash
poetry run python -m admin.admin delete-job-files --directory .
~~~

**Assign a Job:**

~~~bash
poetry run python -m admin.admin assign-job <job_id> <consumer_id>
~~~


---

## Additional Commands

**Start Multiple Consumers:**  
This might be supported via a consumer manager script or adjustments to Supervisor configuration.

**Kill a Consumer Process:**

~~~bash
supervisorctl stop consumer_00
~~~

**Monitor All Processes:**

~~~bash
supervisorctl status
~~~

---

## Additional Notes

- **Process Management:**  
  Supervisor ensures that Producer and Consumer processes remain operational by automatically restarting them if they crash.
- **Logging:**  
  Logs from all components are captured via Supervisor, aiding in troubleshooting and monitoring.
- **Testing:**  
  Simulated consumer failures help validate error handling and job resubmission logic.
- **Extensibility:**  
  The modular design allows for easy integration of additional features, such as a web-based admin interface or enhanced logging.
- **Security:**  
  Ensure proper file permissions and access controls are in place for the SQLite database.

---

## Usage Instructions

**Activate the Virtual Environment & Install Dependencies:**

~~~bash
poetry install
~~~

**Configure Environment Variables:**  
Create a `.env` file in the project root with:

~~~ini
QUEUE_DB_FILE=queue.db
MAX_ATTEMPTS=3
TIMEOUT_SECONDS=60
~~~

**Start Supervisor Processes:**

~~~bash
supervisord -c supervisor/supervisord.conf
~~~

**Launch the Ops Dashboard:**

~~~bash
poetry run streamlit run ops/ops.py
~~~

Visit [http://localhost:8501](http://localhost:8501).

**Use the Admin CLI:**  
For example, list jobs:

~~~bash
poetry run python -m admin.admin list-jobs
~~~

**Launch the Interactive Manager (TUI):**

~~~bash
poetry run python -m manager.manager.py
~~~
