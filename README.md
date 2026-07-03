# Async URL Shortener

A simple asynchronous URL Shortener service built with Flask, Redis, Celery, and SQLite.

## Tech Stack
- Python
- Flask
- Redis (Upstash)
- SQLite
- Marshmallow Schema Validation
- Celery

## Setup Instructions

### 1. Clone the repository
git clone https://github.com/Apoo2/url_shortener.git
cd url_shortener

### 2. Create virtual environment
python -m venv venv

### 3. Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

### 4. Install dependencies
pip install -r requirements.txt

### 5. Run Flask app
python app.py

### 6. Run Worker (new terminal)
python worker.py

## API Endpoints

### POST /shorten
Accepts a URL and returns a short code.

Request:
{
    "url": "https://example.com/some/page"
}

Response (202 Accepted):
{
    "message": "URL received and being processed",
    "short_code": "aZ3kD1"
}

### GET /url/<short_code>
Returns URL information for a given short code.

Response (200 OK):
{
    "short_code": "aZ3kD1",
    "original_url": "https://example.com/some/page",
    "status": "active"
}

Response (404 Not Found):
{
    "error": "Short code not found"
}

## Sample cURL Commands

### Shorten a URL:
curl -X POST http://127.0.0.1:5000/shorten \
  -H "Content-Type: application/json" \
  -d "{\"url\": \"https://www.google.com\"}"

### Get URL info:
curl http://127.0.0.1:5000/url/<short_code>

## Database Schema
Table: urls
- id: Integer (Primary Key, Auto Increment)
- short_code: VARCHAR(10) (Unique)
- original_url: VARCHAR(255) (Not Null)
- status: VARCHAR(20) (pending/active/invalid)

## How it Works
1. User sends POST request with URL
2. Flask generates unique short code
3. Record saved to SQLite with status "pending"
4. Message published to Redis queue
5. Worker picks up message from Redis
6. Worker validates the URL
7. Worker updates status to "active" or "invalid"
8. User can check status via GET endpoint