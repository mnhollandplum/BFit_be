from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from models import User, Post

app = Flask(__name__)



@app.route("/")
def hello():
    return "Hello World!"

@app.route('/about')
def about():
    return "Yo its ya boi.... skinny....."

if __name__ == '__main__':
    app.run(debug=True)
