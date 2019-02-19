from datetime import datetime
from app import app
from app import db
from app.models import User
from app.models import Post
from app.models import Meal
from app.models import Food
from app.models import Exercise
from app.error import bad_request
from flask import jsonify
from flask_sqlalchemy import SQLAlchemy
from flask import request
from IPython import embed
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
    return jsonify(user)

@app.route('/api/v1/posts', methods=['POST'])
def add_post():
    post_data = json.loads(request.get_data())
    if 'title' not in post_data:
        return bad_request("A post title is required.")
    else:
        if 'muscle_group' in post_data:
            post = Post(post_data)
            db.session.add(post)
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
            meal = Meal(post_data, post.id)
            db.session.add(meal)
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
                        'post_id': meal.post_id
                        # 'foods': [{
                        #     'id': food.id,
                        #     'name': food.name,
                        #     'calories': food.calories
                        # }]


                    }
                }
            }
            return jsonify(response)
        else:
            return bad_request("A post title is required.")


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
