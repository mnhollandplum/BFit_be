from datetime import datetime

from app import app
from app import db
from app.models import User
from app.models import Post
from app.error import bad_request
from flask import jsonify
from flask_sqlalchemy import SQLAlchemy
from flask import request
import json

@app.route('/')
@app.route('/index')
def index():
    return "Welcome to the BFit API. Check out our Github for instructions on accessing our endpoints"

@app.route('/api/v1/users', methods=['POST', 'GET'])
def add_user():
    user_data = json.loads(request.get_data())
    if 'username' not in user_data or 'email' not in user_data or 'password' not in user_data:
        return bad_request("Username, email and password are required.")
    if User.query.filter_by(username=user_data['username']).first():
        return bad_request("A username must be unique.")
    if User.query.filter_by(email=user_data['email']).first():
        return bad_request("An email must be unique.")
    else:
        user = User(user_data)
        db.session.add(user)
        db.session.commit()
        response = {
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'avatar': user.avatar
            }
        }
        return jsonify(response)


@app.route('/api/v1/users/<id>', methods=['GET'])
def get_user(id):
    user = User.query.filter_by(id=id).first_or_404()
    response = {'user': {
    'id': user.id,
    'username': user.username,
    'email': user.email,
    'avatar': user.avatar
    }}
    return jsonify(response)

if __name__ == '__main__':
  app.run(debug=True)
