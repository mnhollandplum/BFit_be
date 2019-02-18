from app import db
from datetime import datetime
from IPython import embed


class User(db.Model):
    __tablename__ = 'users'
    id          = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username    = db.Column(db.String(200), unique=True, nullable=False)
    email       = db.Column(db.String(200), unique=True, nullable=False)
    avatar      = db.Column(db.String(200), nullable=False, default='default.jpg')
    password    = db.Column(db.String(200), nullable=False)

    def __init__ (self, data):
        self.username   = data['username']
        self.email      = data['email']
        self.avatar     = data['avatar']
        self.password   = data['password']

    def __repr__(self):
        return str({
            'user': {
                'id': self.id,
                'username': self.username,
                'email': self.email,
                'avatar': self.avatar
            }
        })

class Post(db.Model):
    __tablename__ = 'posts'
    id          = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title       = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    image_url   = db.Column(db.String(400))
    date        = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    post_type   = db.Column(db.String)
    user_id     = db.Column(db.Integer, db.ForeignKey('users.id'))


    def __init__ (self, data):
        self.title          = data['title']
        self.description    = data['description']
        self.image_url      = data['image_url']
        self.date           = data.get('date')
        self.post_type      = data['post_type']
        self.user_id        = data['user_id']

    def __repr__(self):
        return '<Post {}>'.format(self.title)

class Exercise(db.Model):
    __tablename__ = 'exercises'
    id              = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name            = db.Column(db.String(200), nullable=False)
    muscle_group    = db.Column(db.String(200), nullable=False)
    reps            = db.Column(db.Integer, nullable=True)
    weight          = db.Column(db.Integer, nullable=True)
    time            = db.Column(db.Integer, nullable=True)
    distance        = db.Column(db.Integer, nullable=True)
    post_id         = db.Column(db.Integer, db.ForeignKey('posts.id'))


    def __init__ (self, data, post_id):
        self.name           = data['name']
        self.muscle_group   = data['muscle_group']
        self.post_id        = post_id
        if data['muscle_group'] == 'cardio':
            self.time       = data['time']
            self.distance   = data['distance']
        else:
            self.reps       = data['reps']
            self.weight     = data['weight']

    def __repr__(self):
        return '<Exercise {}>'.format(self.name)
