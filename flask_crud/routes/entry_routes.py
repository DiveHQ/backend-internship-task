from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from flask_crud import db, create_app
from flask_crud.models.user import User
from flask_crud.models.entry import Entry
from flask_crud.models.setting import Setting
from flask_crud.utils.helpers import EntrySchema, EntryUpdateSchema, token_required

from nutritionix.nutritionix import NutritionixClient
import jwt
from datetime import datetime

app = create_app("development")

entry_blueprint = Blueprint('entry', __name__)

nutritionix = NutritionixClient(
    application_id=app.config['NUTRITIONIX_APP_ID'],
    api_key=app.config['NUTRITIONIX_API_KEY'],
)


def calculate_total_calories(user_id, date):
    entries = Entry.query.filter_by(user_id=user_id, date=date).all()
    return sum(entry.calories for entry in entries)


def update_entries_below_expected(user_id, date, expected_calories):
    entries = Entry.query.filter_by(user_id=user_id, date=date).all()
    for entry in entries:
        entry.is_below_expected = entry.calories <= expected_calories
        db.session.commit()



@entry_blueprint.route('/entries', methods=['POST'])
@token_required
def create_entry(user_data):
    schema = EntrySchema()
    data = request.get_json()
    try:
        current_user_id = user_data.id
        data = schema.load(data)
    except ValidationError as e:
        return jsonify({'message': e.messages}), 400
    try:
        if data.get('calories') is None:
            response = nutritionix.search(query=data.get('text'))
            data['calories'] = response['branded'][0]['nf_calories']

        user_settings = Setting.query.filter_by(user_id=current_user_id).first()

        entry = Entry(
            user_id=current_user_id,
            text=data.get('text'),
            calories=data.get('calories'),
            is_below_expected=False  # Set to False initially
        )
        db.session.add(entry)
        db.session.commit()

        # Now calculate the total calories and update is_below_expected
        today = datetime.now().date()
        total_calories_today = calculate_total_calories(current_user_id, today)

        if user_settings and user_settings.expected_calories_per_day is not None:
            is_below_expected = total_calories_today <= user_settings.expected_calories_per_day
            entry.is_below_expected = is_below_expected
            db.session.commit()

        return jsonify({'message': 'Entry created successfully', 'entry': entry.to_dict()}), 201
    except Exception as e:
        print(f'An error occurred: {e}')
        return jsonify({'message': 'Create Entry Failed'}), 500


@entry_blueprint.route('/entries', methods=['GET'])
@token_required
def get_entries(user_data):
    current_user_id = user_data.id

    page = request.args.get('page', 1, type=int)  # default page is 1
    per_page = request.args.get(
        'per_page', 10, type=int)  # default per_page is 10

    # Filter: date
    date_filter = request.args.get('date', None)  # default is None
    if date_filter:
        # Assuming date is in 'YYYY-MM-DD' format
        date_filter = datetime.strptime(date_filter, '%Y-%m-%d').date()

    if user_data.role.name == 'admin':
        # If the user is an admin, get all entries
        if date_filter:
            entries = Entry.query.filter_by(date=date_filter).paginate(
                page=page, per_page=per_page, error_out=False)
        else:
            entries = Entry.query.paginate(page=page, per_page=per_page, error_out=False)
    else:
        # Otherwise, get only the user's entries
        if date_filter:
            entries = Entry.query.filter_by(user_id=current_user_id, date=date_filter).paginate(
                page=page, per_page=per_page, error_out=False)
        else:
            entries = Entry.query.filter_by(user_id=current_user_id).paginate(
                page=page, per_page=per_page, error_out=False)

    entries_list = [entry.to_dict() for entry in entries.items]

    return jsonify({
        'entries': entries_list,
        'total_pages': entries.pages,
        'current_page': entries.page
    }), 200

@entry_blueprint.route('/entries/user/<user_id>', methods=['GET'])
@token_required
def get_user_entries(user_data, user_id):
    # Check if the current user has the role to access the entries of the user with user_id
    # The user is allowed if they are an admin or if they are requesting their own entries
    if user_data.role.name != 'admin' and user_data.id != int(user_id):
        return jsonify({'message': 'Access denied'}), 403

    page = request.args.get('page', 1, type=int)  # default page is 1
    per_page = request.args.get('per_page', 10, type=int)  # default per_page is 10

    # Filter: date
    date_filter = request.args.get('date', None)  # default is None
    if date_filter:
        # Assuming date is in 'YYYY-MM-DD' format
        date_filter = datetime.strptime(date_filter, '%Y-%m-%d').date()

    if date_filter:
        entries = Entry.query.filter_by(user_id=user_id, date=date_filter).paginate(
            page=page, per_page=per_page, error_out=False)
    else:
        entries = Entry.query.filter_by(user_id=user_id).paginate(
            page=page, per_page=per_page, error_out=False)

    entries_list = [entry.to_dict() for entry in entries.items]

    return jsonify({
        'entries': entries_list,
        'total_pages': entries.pages,
        'current_page': entries.page
    }), 200


@entry_blueprint.route('/entries/<entry_id>', methods=['PUT'])
@token_required
def update_entry(user_data, entry_id):
    current_user_id = user_data.id
    data = request.get_json()

    # entry = Entry.query.get(entry_id)
    entry = db.session.get(Entry, entry_id)
    if not entry or (entry.user_id != current_user_id and (user_data.role.name != 'admin')):
        return jsonify({'message': 'Entry not found'}), 404

    entry.date = data.get('date', entry.date)
    entry.time = data.get('time', entry.time)
    entry.text = data.get('text', entry.text)
    entry.calories = data.get('calories', entry.calories)

    total_calories_today = calculate_total_calories(
        current_user_id, entry.date)

    user_settings = Setting.query.filter_by(user_id=current_user_id).first()

    is_below_expected = True
    if user_settings and user_settings.expected_calories_per_day is not None:
        is_below_expected = total_calories_today <= user_settings.expected_calories_per_day

    entry.is_below_expected = is_below_expected

    db.session.commit()

    return jsonify({'message': 'Entry updated successfully', 'entry': entry.to_dict()}), 200


@entry_blueprint.route('/entries/<entry_id>', methods=['DELETE'])
@token_required
def delete_entry(user_data, entry_id):
    current_user_id = user_data.id
    # entry = Entry.query.get(entry_id)
    entry = db.session.get(Entry, entry_id)
    if not entry or (entry.user_id != current_user_id and user_data.role.name != 'admin'):
        return jsonify({'message': 'Entry not found'}), 404

    db.session.delete(entry)
    db.session.commit()

    return jsonify({'message': 'Entry deleted successfully'}), 200


def get_user_from_token(token):
    try:
        data = jwt.decode(
            token, app.config['JWT_SECRET_KEY'], algorithms=["HS256"])
        user_id = data['user_id']
    except:
        return jsonify({'message': 'Token is invalid!'}), 401

    # user = User.query.get(user_id)
    user = db.session.get(User, user_id)
    if not user:
        return jsonify({'message': 'User not found!'}), 401

    return user
