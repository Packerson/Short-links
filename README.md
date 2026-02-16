# Short Links

## Endpoints

### 1) Shorten URL
- **Method:** `POST`
- **Path:** `api/v1/short/to_shorten/`
- **Description:** Receives a long URL in the request body, creates a shortened URL, saves the mapping in the database, and returns the shortened URL as JSON.

**Example**

Request:
`{"original_url": "https://www.django-rest-framework.org/VeryLongUrl"}`

Response:
`{"short_url": "http://localhost:8000/api/short/to_read/Ab12Cd"}`

### 2) Resolve URL
- **Method:** `GET`
- **Path:** `api/short/to_read/<code>/`
- **Description:** Reads the short code from the URL path, looks it up in the database, and returns the original URL as JSON.

**Example**


Response:
`{"original_url": "https://www.django-rest-framework.org/VeryLongUrl"}`

## Tech Stack
- Python 3.11+
- Django 5.2
- Django REST Framework
- SQLite
- pytest

## Why SQLite?
- The goal is to keep the project simple. In a production environment, I would use PostgreSQL.

## Why GET for reading?
- The short code is part of the path (`/api/short/to_read/<code>/`), so GET is the simplest API-only contract.


## Without logging
## Without additionsal validation


## TODO:
- pytest
- unit tests
- e2e