from datetime import datetime
from flask import Flask
from flask import request
from flask import jsonify
from flask_sqlalchemy import SQLAlchemy
from IPython import embed


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/bfit'
db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(200), unique=True, nullable=False)
    email = db.Column(db.String(200), unique=True, nullable=False)
    avatar = db.Column(db.String(200), nullable=False, default='default.jpg')
    password = db.Column(db.String(200), nullable=False)

    def __init__ (self, data):
        self.username = data['username']
        self.email = data['email']
        self.avatar = data['avatar']
        self.password = data['password']

    def __repr__(self):
        return f"<User: {self.id}"
    # posts = db.relationship('Post', backref='author', lazy=True)
    # comments = db.relationship('Comment', backref='author', lazy=True)

@app.route("/")
def hello():
    return "<h1>Welcome to BFit API</h1>"

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

if __name__ == '__main__':
  app.run(debug=True)
