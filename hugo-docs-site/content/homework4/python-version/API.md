# API Documentation for Python Version

## Overview

This document provides the API specifications for the Python version of the project. It outlines the available endpoints, request methods, parameters, and response formats.

## Base URL

The base URL for accessing the API is:

```
http://<your-domain>/api/v1/
```

## Endpoints

### 1. Get All Items

- **Endpoint:** `/items`
- **Method:** `GET`
- **Description:** Retrieves a list of all items.
- **Response:**
  - **200 OK**
    ```json
    [
      {
        "id": 1,
        "name": "Item 1",
        "description": "Description of Item 1"
      },
      {
        "id": 2,
        "name": "Item 2",
        "description": "Description of Item 2"
      }
    ]
    ```

### 2. Get Item by ID

- **Endpoint:** `/items/{id}`
- **Method:** `GET`
- **Description:** Retrieves a specific item by its ID.
- **Parameters:**
  - `id` (path) - The ID of the item to retrieve.
- **Response:**
  - **200 OK**
    ```json
    {
      "id": 1,
      "name": "Item 1",
      "description": "Description of Item 1"
    }
    ```
  - **404 Not Found**
    ```json
    {
      "error": "Item not found"
    }
    ```

### 3. Create a New Item

- **Endpoint:** `/items`
- **Method:** `POST`
- **Description:** Creates a new item.
- **Request Body:**
  ```json
  {
    "name": "New Item",
    "description": "Description of the new item"
  }
  ```
- **Response:**
  - **201 Created**
    ```json
    {
      "id": 3,
      "name": "New Item",
      "description": "Description of the new item"
    }
    ```

### 4. Update an Item

- **Endpoint:** `/items/{id}`
- **Method:** `PUT`
- **Description:** Updates an existing item.
- **Parameters:**
  - `id` (path) - The ID of the item to update.
- **Request Body:**
  ```json
  {
    "name": "Updated Item",
    "description": "Updated description"
  }
  ```
- **Response:**
  - **200 OK**
    ```json
    {
      "id": 1,
      "name": "Updated Item",
      "description": "Updated description"
    }
    ```

### 5. Delete an Item

- **Endpoint:** `/items/{id}`
- **Method:** `DELETE`
- **Description:** Deletes an item by its ID.
- **Parameters:**
  - `id` (path) - The ID of the item to delete.
- **Response:**
  - **204 No Content**

## Error Handling

All error responses will include a standard error format:

```json
{
  "error": "Error message"
}
```

## Conclusion

This API documentation provides a comprehensive overview of the available endpoints for the Python version of the project. For further details, please refer to the implementation code or contact the development team.