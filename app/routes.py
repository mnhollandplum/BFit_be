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
@app.route('/')
@app.route('/index')
def index():
    return "Welcome to the BFit API. Check out our Github for instructions on accessing our endpoints"

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


@app.route('/api/v1/users/<id>', methods=['GET'])
def get_user(id):
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


@app.route('/api/v1/users/<id>/posts', methods=['GET'])
def get_user_posts(id):
    user = User.query.filter_by(id=id).first_or_404()
    post_obs = Post.query.filter_by(user_id=id)
    response = {
        'username': user.username,
        'posts': posts_list(post_obs)
    }
    return jsonify(response)


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
            return bad_request("A post title is required.")

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

    # if post.meals.all() == []:
    #     exerices = post.exercises.all()
    # elif post.exercises.all() == []:
    #     meals = post.meals.all()
    # embed()

@app.route('/api/v1/follow/<username>')
# @login_required
def follow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('User {} not found.'.format(username))
        return redirect(url_for('index'))
    if user == current_user:
        flash('You cannot follow yourself!')
        return redirect(url_for('user', username=username))
    current_user.follow(user)
    db.session.commit()
    flash('You are following {}!'.format(username))
    return redirect(url_for('user', username=username))

@app.route('/api/v1/unfollow/<username>')
# @login_required
def unfollow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('User {} not found.'.format(username))
        return redirect(url_for('index'))
    if user == current_user:
        flash('You cannot unfollow yourself!')
        return redirect(url_for('user', username=username))
    current_user.unfollow(user)
    db.session.commit()
    flash('You are not following {}.'.format(username))
    return redirect(url_for('user', username=username))

if __name__ == '__main__':
  app.run(debug=True)
