# What is an API?
API stands for Application Programming Interface  
It acts as a two-way communication bridge between frontend and backend

## What is REST API
- *Rest* stands for Representational State Transfer
- It organizes how the web applications talk to each other, separating what the user sees (frontend) and what runs behind the scenes (backend). 

## Core Principles of REST
1. **Stateless:** The server does not store any information about the client between requests.
2. **Client-Server Architecture:** The app (client) asks for things (data) and the server does what's requested (sends data or makes changes).
3. **Standardized Interface:** REST APIs rely on a set of standard methods (GET, POST, PUT, ,PATCH, DELETE) for interacting with resources (*RESTful Operations*).
     - GET - Retrieve data (e.g., fetch a list or item)
     - POST - Create a new resource
     - PUT - Update an entire existing resource
     - PATCH - Partially update an existing resource
     - DELETE - Delete a resource
4. **Easy-to-Read Data:** REST APIs returns the response in a standardized easy to read formats, typically JSON or XML formats.
