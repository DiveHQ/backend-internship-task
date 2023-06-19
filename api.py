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

# Database Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(20), nullable=False)
    expected_calories = db.Column(db.Integer)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))

class CalorieEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)
    text = db.Column(db.String(100))
    calories = db.Column(db.Integer)
    is_below_expected = db.Column(db.Boolean, default=False)

# Authentication Decorator
def authenticate(role):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            auth_header = request.headers.get('Authorization')
            if not auth_header:
                return jsonify({'message': 'Authorization required'}), 401
            
            try:
                token = auth_header.split(' ')[1]
                payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
                user_id = payload['user_id']
                user = User.query.get(user_id)
                if not user or user.role != role:
                    return jsonify({'message': 'Unauthorized'}), 401
                return func(*args, **kwargs)
            except jwt.ExpiredSignatureError:
                return jsonify({'message': 'Token has expired'}), 401
            except (jwt.InvalidTokenError, IndexError):
                return jsonify({'message': 'Invalid token'}), 401
        return wrapper
    return decorator

# Placeholder functions
def get_calories_from_api(text):
    # Replace with your implementation to get calories from an API
    response = requests.get(f'https://your-api-url.com/calories?text={text}')
    if response.status_code == 200:
        data = response.json()
        calories = data.get('calories', 0)
        return calories
    else:
        return 0

def get_total_calories_for_day(user_id, date):
    # Replace with your implementation to get the total calories for a user on a specific day
    total_calories = CalorieEntry.query.with_entities(db.func.sum(CalorieEntry.calories)).filter_by(user_id=user_id, date=date).scalar()
    return total_calories or 0

def get_expected_calories(user_id):
    # Replace with your implementation to get the expected calories for a user
    user = User.query.get(user_id)
    if user:
        return user.expected_calories or 0
    else:
        return 0

def get_user_id_from_token():
    auth_header = request.headers.get('Authorization')
    token = auth_header.split(' ')[1]
    payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
    user_id = payload['user_id']
    return user_id

# Routes
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    role = data.get('role')
    expected_calories = data.get('expected_calories')

    if not username or not password or not role or not expected_calories:
        return jsonify({'message': 'Missing required fields'}), 400

    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return jsonify({'message': 'Username already exists'}), 409

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

    new_user = User(
        username=username,
        password=hashed_password,
        role=role,
        expected_calories=expected_calories
    )
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User registered successfully'})

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'message': 'Missing username or password'}), 400

    user = User.query.filter_by(username=username).first()
    if not user or not bcrypt.check_password_hash(user.password, password):
        return jsonify({'message': 'Invalid credentials'}), 401

    token = jwt.encode(
        {'user_id': user.id, 'exp': datetime.utcnow() + timedelta(hours=2)},
        app.config['SECRET_KEY'],
        algorithm='HS256'
    )

    return jsonify({'token': token})

@app.route('/entries', methods=['POST'])
@authenticate('regular')
def create_entry():
    data = request.get_json()
    user_id = get_user_id_from_token()

    date_str = data.get('date')
    time_str = data.get('time')
    text = data.get('text')
    calories = data.get('calories')

    if not date_str or not time_str or not text:
        return jsonify({'message': 'Missing required fields'}), 400

    try:
        date = datetime.strptime(date_str, '%Y-%m-%d').date()
        time = datetime.strptime(time_str, '%H:%M:%S').time()
    except ValueError:
        return jsonify({'message': 'Invalid date or time format'}), 400

    if not calories:
        calories = get_calories_from_api(text)

    total_calories = get_total_calories_for_day(user_id, date)
    expected_calories = get_expected_calories(user_id)
    is_below_expected = total_calories < expected_calories

    new_entry = CalorieEntry(
        user_id=user_id,
        date=date,
        time=time,
        text=text,
        calories=calories,
        is_below_expected=is_below_expected
    )
    db.session.add(new_entry)
    db.session.commit()

    return jsonify({'message': 'Entry created successfully'})

@app.route('/entries/<int:entry_id>', methods=['GET'])
@authenticate('regular')
def get_entry(entry_id):
    user_id = get_user_id_from_token()

    entry = CalorieEntry.query.filter_by(id=entry_id, user_id=user_id).first()
    if not entry:
        return jsonify({'message': 'Entry not found'}), 404

    entry_data = {
        'id': entry.id,
        'user_id': entry.user_id,
        'date': entry.date.strftime('%Y-%m-%d'),
        'time': entry.time.strftime('%H:%M:%S'),
        'text': entry.text,
        'calories': entry.calories,
        'is_below_expected': entry.is_below_expected
    }

    return jsonify(entry_data)

if __name__ == '__main__':
    app.run()
