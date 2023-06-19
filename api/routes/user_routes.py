from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token
from api.database import db
from api.models.user import User
from api.schemas.user_schema import UserSchema, UserSchema

from api.utils import get_calories_from_nutritionix_api

user_blueprint = Blueprint('user', __name__)


@user_blueprint.route('/register', methods=['POST'], endpoint='register_user')
def register_user():
    try:
        username = request.json['username']
        password = request.json['password']
        role = 'regular'
        calorie_perday = request.json['calorie_perday']

        new_user = User(username=username, password=password, role=role, calorie_perday=calorie_perday)
        db.session.add(new_user)
        db.session.commit()

        return jsonify({'message': 'Registration successful'}), 200

    except KeyError:
        return jsonify({'message': 'Invalid request body'}), 400

    except Exception as e:
        return jsonify({'message': 'Internal server error'}), 500


@user_blueprint.route('/login', methods=['POST'], endpoint='login_user')
def login_user():
    try:
        username = request.json['username']
        password = request.json['password']

        user = User.query.filter_by(username=username).first()

        if user and user.password == password:
            access_token = create_access_token(identity=user.id)
            return jsonify({'access_token': access_token})

        return jsonify({'message': 'Invalid username or password'}), 401

    except KeyError:
        return jsonify({'message': 'Invalid request body'}), 400

    except Exception as e:
        return jsonify({'message': 'Internal server error'}), 500


@user_blueprint.route('/users', methods=['GET'], endpoint="get_users")
@jwt_required()
def get_users():
    try:
        users = User.query.all()
        return jsonify(UserSchema().dump(users, many=True))

    except Exception as e:
        return jsonify({'message': 'Internal server error'}), 500


@user_blueprint.route('/user/<int:id>', methods=['GET'], endpoint="get_user")
@jwt_required()
def get_user(id):
    try:
        user = User.query.get(id)
        if not user:
            return jsonify({'message': 'User not found'}), 404

        return jsonify(UserSchema().dump(user))

    except Exception as e:
        return jsonify({'message': 'Internal server error'}), 500


@user_blueprint.route('/user/<int:id>', methods=['PUT'], endpoint="update_user")
@jwt_required()
def update_user(id):
    try:
        user = User.query.get(id)
        if not user:
            return jsonify({'message': 'User not found'}), 404

        current_user_id = get_jwt_identity()
        if user.id != current_user_id:
            return jsonify({'message': 'Unauthorized'}), 401

        user.username = request.json['username']
        user.password = request.json['password']
        user.calorie_perday = request.json['calorie_perday']
        db.session.add(user)
        db.session.commit()

        return jsonify({'message': 'Update User successful'}), 200

    except KeyError:
        return jsonify({'message': 'Invalid request body'}), 400

    except Exception as e:
        return jsonify({'message': 'Internal server error'}), 500


@user_blueprint.route('/user/<int:id>', methods=['DELETE'], endpoint="delete_user")
@jwt_required()
def delete_user(id):
    try:
        user = User.query.get(id)
        if not user:
            return jsonify({'message': 'User not found'}), 404

        current_user_id = get_jwt_identity()
        if user.id != current_user_id:
            return jsonify({'message': 'Unauthorized'}), 401

        db.session.delete(user)
        db.session.commit()

        token = create_access_token(identity=current_user_id, fresh=False, expires_delta=False)
        response = jsonify({'message': 'User deleted'})
        response.set_cookie('access_token_cookie', token, httponly=True)

        return response

    except Exception as e:
        return jsonify({'message': 'Internal server error'}), 500
