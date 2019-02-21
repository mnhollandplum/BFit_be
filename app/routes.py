from datetime import datetime
from app import app
from app import db
from app.models import User
from app.models import Post
from app.models import Meal
from app.models import Food
from app.models import Exercise
from app.models import mealfoods
from app.error import bad_request
from flask import jsonify
from flask_sqlalchemy import SQLAlchemy
from flask import request
from IPython import embed
import json


# route helpers
def get_foods(args):
    food_items = []
    for food in args:
        food_response = {'id': food.id, 'name': food.name, 'calories': food.calories}
        food_items.append(food_response)
    return (food_items)


def posts_list(args):
    post_items = []
    for post in args:
        post_response = {
            'id': post.id,
            'title': post.title,
            'description': post.description,
            'image_url': post.image_url,
            'post_type': post.post_type,
            'user_id': post.user_id
        }
        post_items.append(post_response)
    return (post_items)


# Routes

#root
@app.route('/')
@app.route('/index')
def index():
    return "Welcome to the BFit API. Check out our https://github.com/mnhollandplum/BFit_be for instructions on accessing our endpoints and contributing to our project"


#create a user
@app.route('/api/v1/users', methods=['POST'])
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


# user login
@app.route('/api/v1/login', methods=['GET'])
def user_login():
    login_data = json.loads(request.get_data())
    user = User.query.filter_by(username=login_data['user']['username'].lower()).first()
    if user:
        if user.password == login_data['user']['password']:
            return jsonify({
                'user_id': user.id
            })
        else:
            return bad_request("Your username or password was incorrect, try again.")
    else:
        return bad_request("Your username or password was incorrect, try again.")


#edit a user
@app.route('/api/v1/users/<id>/edit', methods=['PUT'])
def update_user(id):
    user = User.query.filter_by(id=id).first_or_404()
    updated_data = json.loads(request.get_data())

    user.avatar = updated_data['avatar']
    db.session.commit()

    return jsonify(updated_data)

#get all users
@app.route('/api/v1/users', methods=['GET'])
def get_users():
    username_query = request.args.get('username')
    users = []
    if username_query:
        user_obs = User.query.filter(User.username.ilike(f'%{username_query}%')).all()
    else:
        user_obs = User.query.all()

    for user in user_obs:
        response = {
            'users': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'avatar': user.avatar
            }
        }
        users.append(response)
    return jsonify(users)


#get a single user by id
@app.route('/api/v1/users/<id>', methods=['GET'])
def get_user_id(id):
    user = User.query.filter_by(id=id).first_or_404()
    response = {
        'user': {
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'avatar': user.avatar
        }
    }
    return jsonify(response)


# current user follows another user
@app.route('/api/v1/users/<user_id>/follow/<id>', methods=['POST'])
def follow_user(user_id, id):
    current_user = User.query.filter_by(id=user_id).first_or_404()
    followed = User.query.filter_by(id=id).first_or_404()
    # create association
    current_user.follow(followed)
    db.session.commit()
    response = "{} is now following {}!".format(current_user.username, followed.username)
    return jsonify(response)


# current user unfollows another user
@app.route('/api/v1/users/<user_id>/unfollow/<id>', methods=['POST'])
def unfollow_user(user_id, id):
    current_user = User.query.filter_by(id=user_id).first_or_404()
    unfollowed = User.query.filter_by(id=id).first_or_404()
    # create association
    current_user.unfollow(unfollowed)
    db.session.commit()
    response = "{} is no longer following {}.".format(current_user.username, unfollowed.username)
    return jsonify(response)


# get a list of users that current user is following
@app.route('/api/v1/users/<id>/following', methods=['GET'])
def get_following(id):
    current_user = User.query.filter_by(id=id).first_or_404()
    user_obs = current_user.followed.all()
    users = []
    for user in user_obs:
        response = {
            'users': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'avatar': user.avatar
            }
        }
        users.append(response)
    return jsonify(users)


# get a list of user who follow current user
@app.route('/api/v1/users/<id>/followers', methods=['GET'])
def get_followers(id):
    user = User.query.filter_by(id=id).first_or_404()
    response = "something"
    return jsonify(response)


#get all posts and all data based on user id
@app.route('/api/v1/users/<id>/posts', methods=['GET'])
def get_user_posts(id):
    user = User.query.filter_by(id=id).first_or_404()
    post_obs = Post.query.filter_by(user_id=id)
    all_posts = []
    if post_obs.all() == []:
        return bad_request("{} has no posts".format(user.username))
    else:
        for post in post_obs:
            if post.meals.all() == []:
                exercise = Exercise.query.filter_by(post_id=post.id).first()
                response = {
                'username': user.username,
                    'post': {
                        'id': post.id,
                        'title': post.title,
                        'description': post.description,
                        'image_url': post.image_url,
                        'user_id': post.user_id,
                        'date': post.date,
                        'post_type': 'exercise',
                        'exercise': {
                            'id': exercise.id,
                            'muscle_group': exercise.muscle_group,
                            'name': exercise.name,
                            'reps': exercise.reps,
                            'weight': exercise.weight,
                            'time': exercise.time,
                            'distance': exercise.distance
                        }
                    }
                }
                all_posts.append(response)
            elif post.exercises.all() == []:
                meal = Meal.query.filter_by(post_id=post.id).first()
                food_obs = meal.foods
                response = {
                'username': user.username,
                    'post': {
                        'id': post.id,
                        'title': post.title,
                        'description': post.description,
                        'image_url': post.image_url,
                        'user_id': post.user_id,
                        'date': post.date,
                        'post_type': 'meal',
                        'meal': {
                            'id': meal.id,
                            'name': meal.name,
                            'foods': get_foods(food_obs)
                        }
                    }
                }
                all_posts.append(response)


    return jsonify(all_posts)

#create a post
@app.route('/api/v1/posts', methods=['POST'])
def add_post():
    post_data = json.loads(request.get_data())
    if 'title' not in post_data:
        return bad_request("A post title is required.")
    else:
        if 'muscle_group' in post_data:
            post = Post(post_data)
            db.session.add(post)
            db.session.commit()
            exercise = Exercise(post_data, post.id)
            db.session.add(exercise)
            db.session.commit()
            response = {
                'post': {
                    'id': post.id,
                    'title': post.title,
                    'description': post.description,
                    'image_url': post.image_url,
                    'user_id': post.user_id,
                    'date': post.date,
                    'post_type': 'exercise',
                    'exercise': {
                        'id': exercise.id,
                        'muscle_group': exercise.muscle_group,
                        'name': exercise.name,
                        'reps': exercise.reps,
                        'weight': exercise.weight,
                        'time': exercise.time,
                        'distance': exercise.distance
                    }
                }
            }
            return jsonify(response)
        elif 'meal' in post_data:
            post = Post(post_data)
            db.session.add(post)
            db.session.commit()
            meal = Meal(post_data, post.id)
            db.session.add(meal)
            db.session.commit()
            foods = post_data['meal']['foods']
            food_obs = []
            for i, x in enumerate(foods, start=0):
                food = Food(foods[i])
                food_obs.append(food)
                db.session.add(food)
                db.session.commit()
                meal.foods.append(food)
                db.session.commit()
            response = {
                'post': {
                    'id': post.id,
                    'title': post.title,
                    'description': post.description,
                    'image_url': post.image_url,
                    'user_id': post.user_id,
                    'date': post.date,
                    'post_type': 'meal',
                    'meal': {
                        'id': meal.id,
                        'name': meal.name,
                        'post_id': meal.post_id,
                        'foods': get_foods(food_obs)
                    }
                }
            }

            return jsonify(response)
        else:
            return bad_request("AHHH! Something went wrong!")

#get a single post based on the id
@app.route('/api/v1/posts/<id>', methods=['GET'])
def get_post(id):
    post = Post.query.filter_by(id=id).first_or_404()
    if post.meals.all() == []:
        exercise = Exercise.query.filter_by(post_id=post.id).first()
        response = {
            'post': {
                'id': post.id,
                'title': post.title,
                'description': post.description,
                'image_url': post.image_url,
                'user_id': post.user_id,
                'date': post.date,
                'post_type': 'exercise',
                'exercise': {
                    'id': exercise.id,
                    'muscle_group': exercise.muscle_group,
                    'name': exercise.name,
                    'reps': exercise.reps,
                    'weight': exercise.weight,
                    'time': exercise.time,
                    'distance': exercise.distance
                }
            }
        }
        return jsonify(response)
    else:
        meal = Meal.query.filter_by(post_id=post.id).first()
        food_obs = meal.foods
        response = {
            'post': {
                'id': post.id,
                'title': post.title,
                'description': post.description,
                'image_url': post.image_url,
                'user_id': post.user_id,
                'date': post.date,
                'post_type': 'meal',
                'meal': {
                    'id': meal.id,
                    'name': meal.name,
                    'foods': get_foods(food_obs)
                }
            }
        }
        return jsonify(response)


@app.route('/api/v1/users/<id>/feed', methods=['GET'])
def get_feed(id):
    user = User.query.filter_by(id=id).first_or_404()
    following = user.followed.all()
    post_obs = []

    for followed in following:
        post_obs = post_obs + followed.posts.all()
    sorted_obs = sorted(post_obs, key=lambda post: post.date , reverse=True)
    all_posts = []

    if sorted_obs == []:
        return bad_request("The users {} is following have no posts".format(user.username))
    else:
        for post in sorted_obs:
            if followed.posts.all() != [] and post.meals.all() == []:
                post_user = User.query.filter_by(id=post.user_id).first()
                exercise = Exercise.query.filter_by(post_id=post.id).first()
                response = {
                    'username': post_user.username,
                    'avatar': post_user.avatar,
                    'post': {
                        'id': post.id,
                        'title': post.title,
                        'description': post.description,
                        'image_url': post.image_url,
                        'user_id': post.user_id,
                        'date': post.date,
                        'post_type': 'exercise',
                        'exercise': {
                            'id': exercise.id,
                            'muscle_group': exercise.muscle_group,
                            'name': exercise.name,
                            'reps': exercise.reps,
                            'weight': exercise.weight,
                            'time': exercise.time,
                            'distance': exercise.distance
                        }
                    }
                }
                all_posts.append(response)
            elif followed.posts.all() != [] and post.exercises.all() == []:
                post_user = User.query.filter_by(id=post.user_id).first()
                meal = Meal.query.filter_by(post_id=post.id).first()
                food_obs = meal.foods
                response = {
                    'username': post_user.username,
                    'avatar': post_user.avatar,
                    'post': {
                        'id': post.id,
                        'title': post.title,
                        'description': post.description,
                        'image_url': post.image_url,
                        'user_id': post.user_id,
                        'date': post.date,
                        'post_type': 'meal',
                        'meal': {
                            'id': meal.id,
                            'name': meal.name,
                            'foods': get_foods(food_obs)
                        }
                    }
                }
                all_posts.append(response)

    return jsonify(all_posts)


if __name__ == '__main__':
  app.run(debug=True)
