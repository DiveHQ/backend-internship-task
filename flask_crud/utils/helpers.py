from marshmallow import Schema, fields
from werkzeug.security import generate_password_hash, check_password_hash
from flask import jsonify, request
from flask_crud import app
from flask_crud.models.user import User
import jwt
from functools import wraps


def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        try:
            auth = request.headers.get('Authorization')
            token = auth.split()[1] if auth else None
            if not token:
                return jsonify({'message': 'Token is missing!'}), 401
            
            user_data = get_user_from_token(token)
            if not user_data:
                return jsonify({'message': 'Invalid token.'}), 401
            return f(user_data, *args, **kwargs)
        except Exception as e:
            print(e)
            return jsonify({'message': 'Invalid token.'}), 401
    
    return decorator

class UserSchema(Schema):
    username = fields.Str(required=True)
    password = fields.Str(required=True)    

    # Add more fields as needed

class UserUpdateSchema(Schema):
    username = fields.Str(required=True)
    # Add more fields as needed


def hash_password(password):
    return generate_password_hash(password, method='scrypt')

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
