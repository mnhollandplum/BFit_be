from datetime import datetime
from flask_io import fields
from sqlalchemy import func
from sqlalchemy_utils.functions import sort_query
from .models import User
from .schemas import UserSchema
from .. import db, io
from flask import Flask

app = Flask(__name__)

app = Blueprint('users', __name__, url_prefix='/api/v1/users'
