# Short Links

## Endpoints

### 1) Shorten URL
- **Method:** `POST`
- **Path:** `api/v1/short/to_shorten`
- **Description:** Receives a long URL in the request body, creates a shortened URL, saves the mapping in the database, and returns the shortened URL as JSON.

**Example**

Request:
`{"original_url": "https://www.django-rest-framework.org/VeryLongUrl"}`

Response:
`{"short_url": "http://localhost:8000/shrt/%5C%60"}`

### 2) Resolve URL
- **Method:** `POST`
- **Path:** `api/v1/short/to_read`
- **Description:** Receives a shortened URL in the request body, looks it up in the database, and returns the original URL.

**Example**

Request:
`{"short_url": "http://localhost:8000/shrt/%5C%60"}`

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

## Why POST in the `to_read` endpoint?
- It reads a shortened URL and returns the original URL in JSON, without automatic redirection.
