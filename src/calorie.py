from flask import Blueprint

calorie = Blueprint("calorie", __name__, url_prefix="/api/v1/calorie")

@calorie.get('/')
def get_all():
    return {"calories": []}

