from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import joinedload
from werkzeug.security import check_password_hash
from flask_crud.models.user import User
from flask_crud.models.role import Role
from flask_crud.utils.helpers import UserSchema, UserUpdateSchema, hash_password, token_required
from flask_crud import db, app
import datetime
import jwt

user_blueprint = Blueprint('user', __name__)

@user_blueprint.route('/register/regular', methods=['POST'])
def register_regular():
    schema = UserSchema()
    data = request.get_json()
    try:
        data = schema.load(data)
    except ValidationError as e:
        return jsonify({'message': e.messages}), 400

    try:
        create_user(data['username'], data['password'], 'regular_user')
        return jsonify({'message': 'New user created! Welcome.'}), 201
    except IntegrityError:
        return jsonify({'message': 'Username already exists.'}), 400
    except Exception:
        return jsonify({'message': 'Registration Failed'}), 500

@user_blueprint.route('/register/admin', methods=['POST'])
def register_admin():
    schema = UserSchema()
    data = request.get_json()
    try:
        data = schema.load(data)
    except ValidationError as e:
        return jsonify({'message': e.messages}), 400

    try:
        create_user(data['username'], data['password'], 'admin')
        return jsonify({'message': 'New Admin created! Welcome.'}), 201
    except IntegrityError:
        return jsonify({'message': 'Username already exists.'}), 400
    except Exception:
        return jsonify({'message': 'Registration Failed'}), 500


@user_blueprint.route('/register/user_manager', methods=['POST'])
def register_user_manager():
    schema = UserSchema()
    data = request.get_json()
    try:
        data = schema.load(data)
    except ValidationError as e:
        return jsonify({'message': e.messages}), 400

    try:
        create_user(data['username'], data['password'], 'regular_user')
        return jsonify({'message': 'New User Manager created! Welcome.'}), 201
    except IntegrityError:
        return jsonify({'message': 'Username already exists.'}), 400
    except Exception:
        return jsonify({'message': 'Registration Failed'}), 500


@user_blueprint.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        user = User.query.filter_by(username=data['username']).first()

        if not user or not check_password_hash(user.password_hash, data['password']):
            return jsonify({'message': 'Login failed, Incorrect login details.'}), 401

        token = jwt.encode({
            'user_id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)  # The token will be expired after 30 mins
        }, app.config['JWT_SECRET_KEY'], algorithm="HS256")


        return jsonify({'message': 'Logged in successfully.', 'token': token}), 200
    except Exception as e:
        print(e)
        return jsonify({'message': 'Login failed.'}), 500


@user_blueprint.route('/users', methods=['POST'])
@token_required
def create_user(user_data):
    if user_data.role.name != 'admin' and user_data.role.name != 'user_manager':
        return jsonify({'message': 'You are not authorized to access this resource.'}), 403
    try:
        schema = UserSchema()
        data = request.get_json()
        try:
            data = schema.load(data)
        except ValidationError as e:
            return jsonify({'message': e.messages}), 400

        hashed_password = hash_password(data['password'])
        role = Role.query.filter_by(name=data['role']).first()

        new_user = User(username=data['username'], password_hash=hashed_password, role=role)
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'message': 'New user created!'}), 201
    except IntegrityError as e:
        print(f"IntegrityError occurred: {e}")
        return jsonify({'message': 'Username already exists.'}), 400
    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({'message': 'Creating a user failed!'}), 500
    

@user_blueprint.route('/users', methods=['GET'])
@token_required
def get_users(user_data):
    if user_data.role.name != 'admin' and user_data.role.name != 'user_manager':
        return jsonify({'message': 'You are not authorized to access this resource.'}), 403
    
    page = request.args.get('page', 1, type=int)  # default page is 1
    per_page = request.args.get('per_page', 10, type=int)  # default per_page is 10

    # Filters
    role_filter = request.args.get('role', None)  # default is None
    
    try:
        query = User.query.options(joinedload(User.role))
        if role_filter:
            role = Role.query.filter_by(name=role_filter).first()
            if role is None:
                return jsonify({'message': 'Role does not exist.'}), 400
            users = query.filter_by(role_id=role.id).paginate(page=page, per_page=per_page, error_out=False)
        else:
            users = query.paginate(page=page, per_page=per_page, error_out=False)

        users_list = [user.to_dict() for user in users.items]

        return jsonify({
            'users': users_list,
            'total_pages': users.pages,
            'current_page': users.page
        }), 200
    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({'message': 'Failed to get users.'}), 500
    
# Get a specific user
@user_blueprint.route('/users/<user_id>', methods=['GET'])
@token_required
def get_user(user_data, user_id):
    if (user_data.role.name != 'admin' and user_data.role.name != 'user_manager') and user_data.id != user_id :
        return jsonify({'message': 'You are not authorized to access this resource.'}), 403

    if user_data.role.name == 'regular_user' and user_data.id == user_id:
        return jsonify(user=user_data.to_dict()), 200
    try:
        user = User.query.get(user_id)
        if user is None:
            return jsonify(message="User not found"), 404
        return jsonify(user=user.to_dict()), 200
    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({'message': 'Failed to get users.'}), 500

# Update a user
@user_blueprint.route('/users/<user_id>', methods=['PUT'])
@token_required
def update_user(user_data, user_id):
    if (user_data.role.name != 'admin' and user_data.role.name != 'user_manager') and user_data.id != user_id :
        return jsonify({'message': 'You are not authorized to access this resource.'}), 403
    try:
        schema = UserUpdateSchema()
        data = request.get_json()
        try:
            data = schema.load(data)
        except ValidationError as e:
            return jsonify({'message': e.messages}), 400
        user = User.query.get(user_id)
        if user is None:
            return jsonify(message="User not found"), 404
        for key, value in data.items():
            setattr(user, key, value)
        db.session.commit()
        return jsonify(message="User updated", user=user.to_dict()), 200
    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({'message': 'Failed to update user.'}), 500

# Delete a user
@user_blueprint.route('/users/<user_id>', methods=['DELETE'])
@token_required
def delete_user(user_data, user_id):
    if (user_data.role.name != 'admin' and user_data.role.name != 'user_manager') and user_data.id != user_id:
        return jsonify({'message': 'You are not authorized to access this resource.'}), 403
    try:
        user = User.query.get(user_id)
        if user is None:
            return jsonify({'message': 'User not found'}), 404
        
        db.session.delete(user)
        db.session.commit()
        return jsonify({'message': 'User deleted'}), 200
    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({'message': 'Failed to delete user.'}), 500



def create_user(username, password, role_name):
    try:
        hashed_password = hash_password(password)
        role = Role.query.filter_by(name=role_name).first()
        new_user = User(username=username, password_hash=hashed_password, role_id=role.id)
        db.session.add(new_user)
        db.session.commit()
        return new_user
    except IntegrityError as e:
        print(f"IntegrityError occurred: {e}")
        raise
    except Exception as e:
        print(f"An error occurred: {e}")
        raise