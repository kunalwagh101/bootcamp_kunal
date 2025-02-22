## Hello World API

### Objective: Create a basic FastAPI app that returns "Hello, World!" on the root path.Task: ####Initialize a FastAPI application and define a route that responds with "Hello, World!".Expected Output: Accessing the root URL displays "Hello, World!".

## CRUD Operations for a Resource

### Objective: Implement CRUD operations for a resource (e.g., items) using FastAPI.
#### Task: Define routes for creating, reading, updating, and deleting items, using an in-memory structure to store them.
#### Expected Output: Functional CRUD operations for items.

## Path and Query Parameters

### Objective: Use path and query parameters in FastAPI routes.
#### Task: Create a route that accepts path parameters for a resource ID and optional query parameters for filtering results.
#### Expected Output: A route that dynamically responds based on provided parameters.


## Request Body and Pydantic Models 

### Objective: Define and use Pydantic models to validate and structure request data.
#### Task: Create a Pydantic model for items and use it in a route to add a new item.
#### Expected Output: Validation and addition of items through the Pydantic model. 

## Database Integration

### Objective: Integrate a simple database (e.g., SQLite) with FastAPI for persisting data.
#### Task: Connect FastAPI to a SQLite database and modify CRUD operations to use the database.
#### Expected Output: CRUD operations interact with a SQLite database. (To add, update, and delete items),

## Background Tasks

### Objective: Utilize background tasks in FastAPI to perform operations after returning a response.
#### Task: Implement a route that initiates a background task for sending an email notification upon completing a certain action.
#### Expected Output: Email notification is sent as a background task.


## File Uploads

### Objective: Handle file uploads in FastAPI.
#### Task: Create a route that allows users to upload files, and save them to a specific directory.
#### Expected Output: Uploaded files are saved to the server.

## Serving Static Files

### Objective: Serve static files, such as images or HTML files, with FastAPI.
#### Task: Configure FastAPI to serve static files from a directory.
#### Expected Output: Static files are accessible via FastAPI. API routes take precedence.
 



## How to run the Api_App


- **cd to Api_app**

```
  cd Api_app
```
- **run the app**
```
    uvicorn main:app --reload

```

## Contains :

- *** main.py     == contain the routes , ex from 1 to 8 ***
- *** models.py   == contain the database ***
- *** database.py == contain the config , also the Question no.5 ***



## Run this urls  to test :

```

/test/create

```

```

```