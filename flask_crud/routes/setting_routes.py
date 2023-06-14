from flask import Blueprint, request, jsonify
from flask_crud import db, create_app
from flask_crud.models.user import User
from flask_crud.models.entry import Entry
from flask_crud.routes.entry_routes import update_entries_below_expected
from flask_crud.utils.helpers import token_required
from flask_crud.models.setting import Setting
from functools import wraps
import jwt
from datetime import datetime

setting_blueprint = Blueprint('setting', __name__)
app = create_app("development")

@setting_blueprint.route('/settings', methods=['POST'])
@token_required
def create_user_settings(user_data):
    current_user_id = user_data.id
    data = request.get_json()

    setting = Setting.query.filter_by(user_id=current_user_id).first()
    if setting:
        return jsonify({'message': 'User settings already exist. Please update existing settings.'}), 400

    expected_calories_per_day = data.get('expected_calories_per_day')

    new_setting = Setting(
        user_id=current_user_id,
        expected_calories_per_day=expected_calories_per_day
    )

    db.session.add(new_setting)
    db.session.commit()

    return jsonify({'message': 'User settings created successfully', 'settings': new_setting.to_dict()}), 201


@setting_blueprint.route('/settings', methods=['GET'])
@token_required
def get_user_settings(user_data):
    current_user_id = user_data.id
    if user_data.role.name == 'admin':
        settings = Setting.query.all()   # If the user is an admin, get all settings
    else:
        # Otherwise, get only the user's settings
        settings = Setting.query.filter_by(user_id=current_user_id).first()

    if not settings:
        return jsonify({'message': 'Settings not found'}), 404

    return jsonify({'settings': settings.to_dict()}), 200


@setting_blueprint.route('/settings', methods=['PUT'])
@token_required
def update_user_settings(user_data):
    current_user_id = user_data.id
    data = request.get_json()

    setting = Setting.query.filter_by(user_id=current_user_id).first()
    if not setting:
        return jsonify({'message': 'User settings not found'}), 404

    setting.expected_calories_per_day = data.get('expected_calories_per_day', setting.expected_calories_per_day)
    db.session.commit()

    # If the user has a daily calorie expectation set, update all entries for today
    if setting.expected_calories_per_day is not None:
        today = datetime.now().date()
        update_entries_below_expected(current_user_id, today, setting.expected_calories_per_day)

    return jsonify({'message': 'User settings updated successfully', 'settings': setting.to_dict()}), 200

@setting_blueprint.route('/settings', methods=['DELETE'])
@token_required
def delete_user_settings(user_data):
    current_user_id = user_data.id
    setting = Setting.query.filter_by(user_id=current_user_id).first()
    if not setting or user_data.role.name != 'admin':
        return jsonify({'message': 'Settings not found'}), 404

    db.session.delete(setting)
    db.session.commit()

    return jsonify({'message': 'Settings deleted successfully'}), 200

def get_user_from_token(token):
    try:
        data = jwt.decode(
            token, app.config['JWT_SECRET_KEY'], algorithms=["HS256"])
        user_id = data['user_id']
    except:
        return jsonify({'message': 'Token is invalid!'}), 401

    user = User.query.get(user_id)
    if not user:
        return jsonify({'message': 'User not found!'}), 401

    return user


