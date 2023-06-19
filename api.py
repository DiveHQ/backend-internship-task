# api.py
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from functools import wraps
import requests
import jwt
from datetime import datetime, timedelta
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from flask_cors import CORS

app = Flask(__name__)
app.config.from_pyfile('config.py')
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
migrate = Migrate(app, db)
CORS(app)
