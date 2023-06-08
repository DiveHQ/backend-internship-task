from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_crud.models.user import User
from flask_crud.models.role import Role
from flask_crud import db, app
from functools import wraps
import datetime
import jwt

user_routes = Blueprint('user_routes', __name__)

def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401
        
        user_data = get_user_from_token(token)
        if not user_data:
            return jsonify({'message': 'Invalid token.'}), 401

        return f(user_data, *args, **kwargs)
    
    return decorator

@user_routes.route('/register/regular', methods=['POST'])
def register_regular():
    try:
        data = request.get_json()

        hashed_password = hash_password(data['password'])
        regular_user_role = Role.query.filter_by(name='regular_user').first()

        new_user = User(username=data['username'], password_hash=hashed_password, role=regular_user_role)
        db.session.add(new_user)
        db.session.commit()

        return jsonify({'message': 'New user created! Welcome.'}), 201
    except:
        return jsonify({'message': 'Registration Failed'}), 500

@user_routes.route('/register/admin', methods=['POST'])
def register_admin():
    try:
        data = request.get_json()

        hashed_password = hash_password(data['password'])
        admin_role = Role.query.filter_by(name='admin').first()

        new_user = User(username=data['username'], password_hash=hashed_password, role=admin_role)
        db.session.add(new_user)
        db.session.commit()

        return jsonify({'message': 'New Admin created! Welcome.'}), 201
    except:
        return jsonify({'message': 'Registration Failed'}), 500

@user_routes.route('/register/user_manager', methods=['POST'])
def register_user_manager():
    try:
        data = request.get_json()

        hashed_password = hash_password(data['password'])
        user_manager_role = Role.query.filter_by(name='user_manager').first()

        new_user = User(username=data['username'], password_hash=hashed_password, role=user_manager_role)
        db.session.add(new_user)
        db.session.commit()

        return jsonify({'message': 'New User Manager created! Welcome.'}), 201
    except:
        return jsonify({'message': 'Registration Failed'}), 500

@user_routes.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        user = User.query.filter_by(username=data['username']).first()

        if not user or not check_password_hash(user.password_hash, data['password']):
            return jsonify({'message': 'Login failed.'}), 401

        token = jwt.encode({
            'user_id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)  # The token will be expired after 30 mins
        }, app.config['JWT_SECRET_KEY'], algorithm="HS256")


        return jsonify({'message': 'Logged in successfully.', 'token': token}), 200
    except:
        return jsonify({'message': 'Login failed.'}), 500


@user_routes.route('/users', methods=['POST'])
@token_required
def create_user(user_data):
    if user_data.role.name != 'admin' and user_data.role.name != 'user_manager':
        return jsonify({'message': 'You are not authorized to access this resource.'}), 403
    try:
        data = request.get_json()

        hashed_password = hash_password(data['password'])
        role = Role.query.filter_by(name=data['role']).first()

        new_user = User(username=data['username'], password_hash=hashed_password, role=role)
        db.session.add(new_user)
        db.session.commit()
    except:
        return jsonify({'message': 'Creating a user failed!'}), 500

    return jsonify({'message': 'New user created!'}), 201

# Get all users
@user_routes.route('/users', methods=['GET'])
@token_required
def get_users(user_data):
    if user_data.role.name != 'admin' and user_data.role.name != 'user_manager':
        return jsonify({'message': 'You are not authorized to access this resource.'}), 403
    try:
        users = User.query.all()
        return jsonify(users=[user.to_dict() for user in users]), 200
    except:
        return jsonify({'message': 'Failed to get users.'}), 500

# Get a specific user
@user_routes.route('/users/<user_id>', methods=['GET'])
@token_required
def get_user(user_data, user_id):
    if (user_data.role.name != 'admin' and user_data.role.name != 'user_manager') and user_data.id != user_id :
        return jsonify({'message': 'You are not authorized to access this resource.'}), 403

    if user_data.role.name == 'regular_user' and user_data.id == user_id:
        return jsonify(user=user_data.to_dict()), 200

    user = User.query.get(user_id)
    if user is None:
        return jsonify(message="User not found"), 404
    return jsonify(user=user.to_dict()), 200

# Update a user
@user_routes.route('/users/<user_id>', methods=['PUT'])
@token_required
def update_user(user_data, user_id):
    if (user_data.role.name != 'admin' and user_data.role.name != 'user_manager') and user_data.id != user_id :
        return jsonify({'message': 'You are not authorized to access this resource.'}), 403

    data = request.get_json()
    user = User.query.get(user_id)
    if user is None:
        return jsonify(message="User not found"), 404
    for key, value in data.items():
        setattr(user, key, value)
    db.session.commit()
    return jsonify(message="User updated", user=user.to_dict()), 200

# Delete a user
@user_routes.route('/users/<user_id>', methods=['DELETE'])
@token_required
def delete_user(user_data, user_id):
    if (user_data.role.name != 'admin' and user_data.role.name != 'user_manager') and user_data.id != user_id:
        return jsonify({'message': 'You are not authorized to access this resource.'}), 403

    user = User.query.get(user_id)
    if user is None:
        return jsonify(message="User not found"), 404
    db.session.delete(user)
    db.session.commit()
    return jsonify(message="User deleted"), 200







def get_user_from_token(token):
    try:
        data = jwt.decode(token, app.config['JWT_SECRET_KEY'], algorithms=["HS256"])
        user_id = data['user_id']
    except:
        return jsonify({'message': 'Token is invalid!'}), 401

    user = User.query.get(user_id)
    if not user:
        return jsonify({'message': 'User not found!'}), 401
    
    return user

def hash_password(password):
    return generate_password_hash(password, method='sha256')






