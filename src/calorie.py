from flask import Blueprint, jsonify, request
from src.database import User, db, Calories
from flask_jwt_extended import get_jwt_identity, jwt_required
import requests

calorie = Blueprint("calorie", __name__, url_prefix="/api/v1/calorie")

def get_authenticated_user_role():
    user_id = get_jwt_identity()
    user = User.query.filter_by(id=user_id).first()
    if user:
        return user.role
    return jsonify({
        'message': 'No role assigned'
    }), 404

def get_authenticated_user():
    user_id = get_jwt_identity()
    user = User.query.filter_by(id=user_id).first()
    if user:
        return jsonify({
            "username": user.username,
            "expected_calories": user.expected_calories
        }), 404
    return None

def is_valid_user(username):
    user = User.query.filter_by(username=username).first()
    return user is not None

def get_user_expected_calories(username):
    user = User.query.filter_by(username=username).first()
    if user:
        return user.expected_calories
    return 0



def fetch_calories_from_api(meal_text):
    url = "https://chomp.p.rapidapi.com/request.php"
    querystring = {"ingredient": meal_text}
    headers = {
        "X-RapidAPI-Key": "eccb9ff5e4msh4e62bb87fac5288p18b969jsna846cf0bda06",
        "X-RapidAPI-Host": "chomp.p.rapidapi.com"
    }

    try:
        response = requests.get(url, headers=headers, params=querystring)
        if response.status_code == 200:
            data = response.json()
            calories = data.get('calories')
            return calories
    except requests.exceptions.RequestException as e:
        
        print(f"Error connecting to Calories API: {e}")

    return None


def calculate_total_calories_less_than_expected(owner, date, new_calories):
    total_calories = sum(
        meal.calorie for meal in Calories.query.filter_by(owner=owner, date=date).all()
    )
    expected_calories = get_user_expected_calories(owner)
    return total_calories < expected_calories



@calorie.route('/', methods=['GET'])
def get_all():
    role = get_authenticated_user_role()

    if role =='regular':
        user = get_authenticated_user()
        user_meals = Calories.query.filter_by(user_id=user['id']).all()
        return jsonify({"meals": [meal.serialize() for meal in user_meals]})
    
    meals = Calories.query.all()
    return jsonify({"meals": [meal.serialize() for meal in meals]}), 200

@calorie.route('/', methods=['POST'])
@jwt_required()
def create ():
    data = request.get_json()
    date = data['created_date']
    time = data['created_time']
    text = data['meal']
    calories = data.get('calories')
    # owner = user['username']

    role = get_authenticated_user_role()

    if role == 'regular':
        user = get_authenticated_user()
        owner = user['username']
        expected_calories = user['expected_calories']
    else:
        owner = data['username']
        expected_calories = get_user_expected_calories(owner)

        if not is_valid_user(owner):
            return jsonify({"message": "Invalid user"}), 400
        
    # If calories are not provided, fetch them from a Calories API provider
    if not calories:
        calories = fetch_calories_from_api(text)
        if calories is None:
            return jsonify({"message": "Failed to fetch calories from API"}), 500
    
    
    is_below_expected = calculate_total_calories_less_than_expected(owner, date, calories)
    new_meal = Calories(
        date=date,
        time=time,
        meal=text,
        calorie=calories,
        user_id=owner,
        is_below_expected=is_below_expected
    )
    db.session.add(new_meal)
    db.session.commit()

    return jsonify({"message": "Meal created successfully", "meal": new_meal.serialize()}), 201


@calorie.route('/<int:meal_id>', methods=['GET'])
def get(meal_id):
    meal = Calories.query.get(meal_id)

    if not meal:
        return jsonify({"message": "Meal not found"}), 404

   
    role = get_authenticated_user_role()

    # Regular users can only access their owned records
    if role == 'regular':
        user = get_authenticated_user()
        if meal.user_id != user['username']:
            return jsonify({"message": "Unauthorized"}), 401

    return jsonify({"meal": meal.serialize()})


@calorie.route('/<int:meal_id>', methods=['PUT'])
def update(meal_id):
    meal = Calories.query.get(meal_id)

    if not meal:
        return jsonify({"message": "Meal not found"}), 404

    data = request.get_json()
    date = data['date']
    time = data['time']
    text = data['text']
    calories = data.get('calories')  # Check if calories are provided

   
    role = get_authenticated_user_role()

    # Regular users can only update their owned records
    if role == 'regular':
        user = get_authenticated_user()
        if meal.user_id != user['username']:
            return jsonify({"message": "Unauthorized"}), 401

        expected_calories = user['expected_calories']
    else:
        expected_calories = get_user_expected_calories(meal.user_id)

    
    if not calories:
        calories = fetch_calories_from_api(text)
        if calories is None:
            return jsonify({"message": "Failed to fetch calories from API"}), 500

    meal.date = date
    meal.time = time
    meal.meal = text
    meal.calorie = calories
    meal.is_below_expected = calculate_total_calories_less_than_expected(meal.user_id, date, calories)

    db.session.commit()

    return jsonify({"message": "Meal updated successfully", "meal": meal.serialize()})


@calorie.route('/<int:meal_id>', methods=['DELETE'])
def delete(meal_id):
    meal = Calories.query.get(meal_id)

    if not meal:
        return jsonify({"message": "Meal not found"}), 404

    role = get_authenticated_user_role()

    if role == 'regular':
        user = get_authenticated_user()
        if meal.user_id != user['username']:
            return jsonify({"message": "Unauthorized"}), 401

    db.session.delete(meal)
    db.session.commit()

    return jsonify({"message": "Meal deleted successfully"})


@calorie.route('/', methods=['POST'])
@jwt_required()
def create():
    data = request.get_json()
    date = data['date']
    time = data['time']
    text = data['text']
    calories = data.get('calories')

    role = get_authenticated_user_role()

    if role == 'regular':
        user = get_authenticated_user()
        owner = user['username']
        expected_calories = user['expected_calories']
    else:
        owner = data['username']
        expected_calories = get_user_expected_calories(owner)

        if not is_valid_user(owner):
            return jsonify({"message": "Invalid user"}), 400

    # If calories are not provided, fetch them from a Calories API provider
    if not calories:
        calories = fetch_calories_from_api(text)
        if calories is None:
            return jsonify({"message": "Failed to fetch calories from API"}), 500

    is_below_expected = calculate_total_calories_less_than_expected(owner, date, calories)
    new_meal = Calories(
        date=date,
        time=time,
        meal=text,
        calorie=calories,
        user_id=owner,
        is_below_expected=is_below_expected
    )
    db.session.add(new_meal)
    db.session.commit()

    return jsonify({"message": "Meal created successfully", "meal": new_meal.serialize()}), 201
