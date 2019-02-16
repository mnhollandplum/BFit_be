from app import app
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

@app.route('/')
@app.route('/index')
def index():
    return "Welcome to the BFit API. Check out our Github for instructions on accessing our endpoints"

@app.route('/api/v1/users', methods=['POST'])
def add_user():
    user = User(request.form)
    db.session.add(user)
    db.session.commit()
    response = {'user': {
    'id': user.id,
    'username': user.username,
    'email': user.email,
    'avatar': user.avatar
    }}
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
