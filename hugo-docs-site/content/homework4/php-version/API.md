# API Documentation for PHP Version

## Overview

This document provides the API specifications for the PHP version of the project. It outlines the available endpoints, their functionalities, and the expected request and response formats.

## Base URL

The base URL for the API is:

```
http://yourdomain.com/api
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
- **Description:** Retrieves a single item by its ID.
- **Parameters:**
  - `id` (integer): The ID of the item to retrieve.
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
  - `id` (integer): The ID of the item to update.
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
  - `id` (integer): The ID of the item to delete.
- **Response:**
  - **204 No Content**

## Conclusion

This API allows for the management of items within the PHP application. Ensure to handle errors appropriately and validate input data when interacting with the API.