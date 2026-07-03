import redis
import json
import requests
import sqlite3
import os
import time

# Redis connection
r = redis.Redis(
    host='fit-cheetah-75981.upstash.io',
    port=6379,
    password='gQAAAAAAASjNAAIgcDJjNjZjMjNlODVkMjM0YTZjYWQ5MTVmYmNhNGUwYzg4Yg',
    ssl=True,
    socket_timeout=10,
    socket_connect_timeout=10
)
# Database path
DB_PATH = os.path.join(os.path.dirname(__file__), 'instance', 'urls.db')

def validate_url(url):
    try:
        response = requests.head(url, timeout=5, allow_redirects=True)
        return response.status_code < 400
    except:
        return False

def update_status(url_id, status):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE urls SET status = ? WHERE id = ?",
        (status, url_id)
    )
    conn.commit()
    conn.close()

def process_message(message):
    data = json.loads(message)
    url_id = data['id']
    url = data['url']
    short_code = data['short_code']
    
    print(f"Processing: {short_code} -> {url}")
    
    # Validate URL
    is_valid = validate_url(url)
    status = 'active' if is_valid else 'invalid'
    
    # Update database
    update_status(url_id, status)
    print(f"Updated {short_code} to status: {status}")

print("Worker started. Waiting for messages...")

# Continuously listen for messages
while True:
    try:
        # Block and wait for message from Redis queue
        message = r.brpop("url_queue", timeout=5)
        if message:
            _, data = message
            process_message(data)
    except Exception as e:
        print(f"Error: {e}")
        time.sleep(2)