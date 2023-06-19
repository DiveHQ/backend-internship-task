from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from api.database import db
from api.models.entry import Entry
from api.schemas.entry_schema import EntrySchema

from api.utils import get_calories_from_nutritionix_api

entry_blueprint = Blueprint('entry', __name__)

@entry_blueprint.route('/entries', methods=['GET'])
@jwt_required()
def get_entries():
    try:
        user_id = get_jwt_identity()
        entries = Entry.query.filter_by(user_id=user_id).all()
        entry_schema = EntrySchema(many=True)
        return jsonify(entry_schema.dump(entries))
    except Exception as e:
        return jsonify({'message': 'Error occurred', 'error': str(e)}), 500

@entry_blueprint.route('/entry/new', methods=['POST'], endpoint="create_entry")
@jwt_required()
def create_entry():
    try:
        user_id = get_jwt_identity()
        text = request.json['text']
        calories = request.json.get('calories')

        if not calories:
            calories = get_calories_from_nutritionix_api(text)

        entry = Entry(user_id=user_id, text=text, calories=calories)
        db.session.add(entry)
        db.session.commit()

        entry_schema = EntrySchema()
        return jsonify(entry_schema.dump(entry))
    except Exception as e:
        return jsonify({'message': 'Error occurred', 'error': str(e)}), 500


@entry_blueprint.route('/entry/<int:id>', methods=['GET'], endpoint="get_entry2")
@jwt_required()
def get_entry2(id):
    try:
        entry = Entry.query.get(id)
        if not entry:
            return jsonify({'message': 'Entry not found'}), 404

        current_user_id = get_jwt_identity()
        if entry.user_id != current_user_id:
            return jsonify({'message': 'Unauthorized'}), 401

        entry_schema = EntrySchema()
        entry_data = entry_schema.dump(entry)
        return jsonify(entry_data)
    except Exception as e:
        return jsonify({'message': 'Error occurred', 'error': str(e)}), 500


@entry_blueprint.route('/entry/<int:id>', methods=['PUT'], endpoint="update_entry")
@jwt_required()
def update_entry(id):
    try:
        entry = Entry.query.get(id)
        if not entry:
            return jsonify({'message': 'Entry not found'}), 404

        current_user_id = get_jwt_identity()
        if entry.user_id != current_user_id:
            return jsonify({'message': 'Unauthorized'}), 401

        entry.text = request.json['text']
        entry.calories = request.json.get('calories')
        db.session.add(entry)
        db.session.commit()

        entry_schema = EntrySchema()
        return jsonify(entry_schema.dump(entry))
    except Exception as e:
        return jsonify({'message': 'Error occurred', 'error': str(e)}), 500



@entry_blueprint.route('/entry/<int:id>', methods=['DELETE'], endpoint="delete_entry")
@jwt_required()
def delete_entry(id):
    try:
        entry = Entry.query.get(id)
        if not entry:
            return jsonify({'message': 'Entry not found'}), 404

        current_user_id = get_jwt_identity()
        auth_header = request.headers.get('Authorization')
        token = auth_header.split()[1] if auth_header else None

        if token:
            current_user_role = "admin"  # Replace with actual role extraction logic

            if current_user_role == 'admin':
                db.session.delete(entry)
                db.session.commit()
                return jsonify({'message': 'Entry deleted'})
            elif current_user_role == 'manager' and entry.user_id == current_user_id:
                db.session.delete(entry)
                db.session.commit()
                return jsonify({'message': 'Entry deleted'})
            else:
                return jsonify({'message': 'Unauthorized'}), 401
        else:
            return jsonify({'message': 'Unauthorized'}), 401

    except Exception as e:
        return jsonify({'message': 'Error occurred', 'error': str(e)}), 500

