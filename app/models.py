from app import db
from datetime import datetime
from IPython import embed


followers = db.Table('followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('users.id'))
)


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(200), unique=True, nullable=False)
    email = db.Column(db.String(200), unique=True, nullable=False)
    avatar = db.Column(db.String(200), nullable=False, default='default.jpg')
    password = db.Column(db.String(200), nullable=False)
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    followed = db.relationship(
        'User', secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        backref=db.backref('followers', lazy='dynamic'), lazy='dynamic')
    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)

    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)

    def is_following(self, user):
        return self.followed.filter(
            followers.c.followed_id == user.id).count() > 0

    def followed_posts(self):
        followed = Post.query.join(
            followers, (followers.c.followed_id == Post.user_id)).filter(
                followers.c.follower_id == self.id)
        own = Post.query.filter_by(user_id=self.id)
        return followed.union(own).order_by(Post.timestamp.desc())


    def __init__ (self, username,email,avatar,password):
        self.username = username
        self.email = email
        self.avatar = avatar
        self.password = password

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


    def __init__ (self, title, description, image_url, date, post_type, user_id):
        self.title          = title
        self.description    = description
        self.image_url      = image_url
        self.date           = date
        self.post_type      = post_type
        self.user_id        = user_id

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


mealfoods = db.Table('mealfoods',
    db.Column('meal_id', db.Integer, db.ForeignKey('meals.id'), primary_key=True),
    db.Column('food_id', db.Integer, db.ForeignKey('foods.id'), primary_key=True)
)

class Meal(db.Model):
    __tablename__ = 'meals'
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))
    name = db.Column(db.String(200), nullable=False)
    date = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    foods = db.relationship('Food', secondary=mealfoods, lazy='subquery',
        backref=db.backref('meals', lazy=True))

    def __init__ (self, name, date, post_id):
        self.name = name
        self.date = date
        self.post_id = post_id

    def __repr__(self):
        return '<Meal {}>'.format(self.name)

class Food(db.Model):
    __tablename__ = 'foods'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    calories = db.Column(db.Integer, nullable=True)

    def __init__ (self, name,calories):
        self.name = name
        self.calories = calories

    def __repr__(self):
        return '<Food {}>'.format(self.name)
