from flask import Blueprint, request, jsonify
from flask_crud import db, app
from flask_crud.models.user import User
from flask_crud.models.entry import Entry
from flask_crud.models.setting import Setting
from functools import wraps

from nutritionix.nutritionix import NutritionixClient
import jwt
import datetime


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


@entry_blueprint.route('/entries', methods=['POST'])
@token_required
def create_entry(user_data):
    current_user_id = user_data.id
    data = request.get_json()

    # check if calories is provided
    if data.get('calories') is None:
        # get the calories data from Nutritionix API
        response = nutritionix.search(q=data.get(
            'text'), limit=1, search_nutrient='calories')
        data['calories'] = response['hits'][0]['fields']['nf_calories']

    today = datetime.today().date()
    total_calories_today = calculate_total_calories(current_user_id, today)

    user_settings = Setting.query.filter_by(user_id=current_user_id).first()

    is_below_expected = True
    if user_settings and user_settings.expected_calories_per_day is not None:
        is_below_expected = total_calories_today <= user_settings.expected_calories_per_day

    entry = Entry(
        user_id=current_user_id,
        date=data.get('date'),
        time=data.get('time'),
        text=data.get('text'),
        calories=data.get('calories'),
        is_below_expected=is_below_expected
    )

    db.session.add(entry)
    db.session.commit()

    return jsonify({'message': 'Entry created successfully', 'entry': entry.to_dict()}), 201


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
                page, per_page, error_out=False)
        else:
            entries = Entry.query.paginate(page, per_page, error_out=False)
    else:
        # Otherwise, get only the user's entries
        if date_filter:
            entries = Entry.query.filter_by(user_id=current_user_id, date=date_filter).paginate(
                page, per_page, error_out=False)
        else:
            entries = Entry.query.filter_by(user_id=current_user_id).paginate(
                page, per_page, error_out=False)

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

    entry = Entry.query.get(entry_id)
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
    entry = Entry.query.get(entry_id)
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

    user = User.query.get(user_id)
    if not user:
        return jsonify({'message': 'User not found!'}), 401

    return user
