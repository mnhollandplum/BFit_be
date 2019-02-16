from app import db
from datetime import datetime

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
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

class Post(db.Model):
    __tablename__ = 'post'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(20))
    description = db.Column(db.String(120))
    image_url = db.Column(db.String(120))
    date = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    post_type = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post {}>'.format(self.title)
