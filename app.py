from flask import Flask, request, jsonify
from models import db, URL
from schemas import URLSchema
from marshmallow import ValidationError
import redis
import json
import random
import string
import os

app = Flask(__name__)

# Database config
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///urls.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database
db.init_app(app)

# Redis connection
r = redis.Redis(
    host='fit-cheetah-75981.upstash.io',
    port=6379,
    password='gQAAAAAAASjNAAIgcDJjNjZjMjNlODVkMjM0YTZjYWQ5MTVmYmNhNGUwYzg4Yg',
    ssl=True,
    socket_timeout=10,
    socket_connect_timeout=10
)

# Schema
url_schema = URLSchema()

def generate_short_code(length=6):
    characters = string.ascii_letters + string.digits
    while True:
        code = ''.join(random.choices(characters, k=length))
        # Make sure code is unique
        if not URL.query.filter_by(short_code=code).first():
            return code

# Create tables
with app.app_context():
    db.create_all()

@app.route('/shorten', methods=['POST'])
def shorten_url():
    # Validate input
    try:
        data = url_schema.load(request.get_json())
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400

    original_url = data['url']

    # Generate short code
    short_code = generate_short_code()

    # Save to database with status pending
    new_url = URL(
        short_code=short_code,
        original_url=original_url,
        status='pending'
    )
    db.session.add(new_url)
    db.session.commit()

    # Publish message to Redis
    message = {
        "id": new_url.id,
        "short_code": short_code,
        "url": original_url
    }
    r.lpush("url_queue", json.dumps(message))

    return jsonify({
        "message": "URL received and being processed",
        "short_code": short_code
    }), 202


@app.route('/url/<short_code>', methods=['GET'])
def get_url(short_code):
    url = URL.query.filter_by(short_code=short_code).first()
    
    if not url:
        return jsonify({"error": "Short code not found"}), 404
    
    return jsonify(url.to_dict()), 200


if __name__ == '__main__':
    app.run(debug=True)