# Event Management API Documentation

This API provides endpoints for managing events, including scheduling, retrieving, updating, and deleting events.

## Authentication

All endpoints, except for the event retrieval endpoints (`GET /events` and `GET /events/<int:event_id>`), require authentication. Authentication is done using a JSON Web Token (JWT). The token should be included in the `x-access-tokens` header of the request.

This API provides endpoints for user registration and login.

## Project Structure

- project - containts:
  - routes
  - models
  - static data
- tests - containts:
  - integration tests
  - unit tests

## Installation

### Prerequisites

#### Make sure you have the following tools installed:

    Docker
    Docker Compose

#### Setup

    Clone the repository:

    bash

    git clone https://github.com/your-username/your-project.git

Navigate to the project directory:

    bash

    cd your-project

Start the application using Docker Compose:

    bash

    docker-compose up --build

The above command will download and build the required images, and then start the containers defined in your docker-compose.yml file.

    Access the application in your web browser:


    https://localhost:5000

That's it! Your application should now be running in a Docker container.

## User Registration Endpoint (`POST /register`)

This endpoint allows users to register by providing their email and password.

### Request

- **Method:** `POST`
- **Endpoint:** `/register`
- **Request Body (JSON):**
  ```json
  {
    "email": "user@example.com",
    "password": "password123"
  }
  ```

### Response

    Status Code: 200 OK
    Body (JSON):

    json

    {
    "message": "Registered successfully"
    }

### Error Response (Email Already Exists):

    json

    {
      "message": "ERROR! Email (user@example.com) already exists in the database."
    }

## User Login Endpoint (POST /login)

This endpoint allows users to log in by providing their email and password.
Request

    Method: POST
    Endpoint: /login
    Request Authorization Header:
        Username: Email
        Password: Password

### Response

    Status Code: 200 OK
    Body (JSON):

    json

    {
    "token": "jwt_token_here"
    }

### Error Response (Invalid Credentials):

    json

    {
    "message": "Could not verify. Login required."
    }

## Token Required Decorator

The `token_required` decorator is used to protect endpoints that require authentication. It checks for a valid JWT in the request headers and retrieves the corresponding user from the database.

```python
@token_required
def some_protected_endpoint(user):
    # ... (implementation)
```

## Error Handling

In case of errors, the API returns a JSON object with a `message` field containing a descriptive error message.

Schedule Event (POST /events)

This endpoint allows users to schedule new events.

### Request

    Method: POST
    Endpoint: /events
    Headers:
        x-access-tokens: JWT for authentication
    Request Body (JSON):

    json

    {
      "title": "Event Title",
      "description": "Event Description",
      "venue": "Event Venue",
      "location": "Event Location",
      "event_date": "YYYY-MM-DD HH:MM:SS",
      "tags": ["tag1", "tag2"],
      "participants": 5
    }

### Response

    Status Code: 201 Created
    Body (JSON):

    json

    {
      "message": "Event scheduled successfully"
    }

## Get Events (GET /events)

This endpoint retrieves a list of events based on query parameters.

### Request

    Method: GET
    Endpoint: /events
    Query Parameters:
        location (optional): Filter events by location
        venue (optional): Filter events by venue
        sort_by (optional): Sort events by "date," "popularity," or "creation_time"

### Response

    Status Code: 200 OK
    Body (JSON):

    json

    {
      "events": [
        {
          "id": 1,
          "title": "Event Title",
          "description": "Event Description",
          "venue": "Event Venue",
          "location": "Event Location",
          "event_date": "YYYY-MM-DD HH:MM:SS",
          "tags": ["tag1", "tag2"],
          "participants": 5
        },
        // ... (additional events)
      ]
    }

## Get Event Details (GET /events/<int:event_id>)

This endpoint retrieves details of a specific event.

### Request

    Method: GET
    Endpoint: /events/<int:event_id>

### Response

    Status Code: 200 OK
    Body (JSON):

    json

    {
      "id": 1,
      "title": "Event Title",
      "description": "Event Description",
      "venue": "Event Venue",
      "location": "Event Location",
      "event_date": "YYYY-MM-DD HH:MM:SS",
      "tags": ["tag1", "tag2"],
      "participants": 5
    }

## Update Event (PUT /events/<int:event_id>)

This endpoint allows the owner of an event to update its details.

### Request

    Method: PUT
    Endpoint: /events/<int:event_id>
    Headers:
        x-access-tokens: JWT for authentication
    Request Body (JSON):

    json

    {
      "description": "Updated Description",
      "venue": "Updated Venue",
      "location": "Updated Location",
      "event_date": "YYYY-MM-DD HH:MM:SS",
      "tags": ["tag1", "tag2"],
      "participants": 10
    }

### Response

    Status Code: 200 OK
    Body (JSON):

    json

    {
      "message": "Event updated successfully"
    }

# Delete Event (DELETE /events/<int:event_id>)

This endpoint allows the owner of an event to delete it.

### Request

    Method: DELETE
    Endpoint: /events/<int:event_id>
    Headers:
        x-access-tokens: JWT for authentication

### Response

    Status Code: 200 OK
    Body (JSON):

    json

    {
    "message": "Event deleted successfully"
    }
