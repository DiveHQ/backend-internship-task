from flask import Blueprint, request, jsonify
from werkzeug.security import check_password_hash, generate_password_hash
import validators
from flask_jwt_extended import create_access_token, create_refresh_token
from src.database import User, db

auth = Blueprint("auth", __name__, url_prefix="/api/v1/auth")

@auth.post('/register')
def register():
    username = request.json['username']
    email = request.json['email']
    password = request.json['password']

    if len(password) < 6:
        return jsonify({'error': "Password is too short"}), 400
    
    if not username.isalnum() or " " in username:
        return jsonify({'error': "Username should be alphanumeric & no spaces are allowed"}), 400
    
    if not validators.email(email):
        return jsonify({'error': "Email is not valid"}), 400
    
    if User.query.filter_by(email=email).first() is not None:
        return jsonify({'error': "Email is already taken"}), 409

    

    if User.query.filter_by(username=username).first() is not None:
        return jsonify({'error': "Username is already taken"}), 409
    

    pwd_hash=generate_password_hash(password)
    user=User(username=username, password=pwd_hash, email=email)

    db.session.add(user)
    db.session.commit()

    return jsonify({
        'message': "User Created",
        'user': {
            'username': username, 'email': email
        }
    }), 201

@auth.post('/login')
def login():
    email = request.json.get('email','')
    password = request.json.get('password','')
    user = User.query.filter_by(email=email).first()

    if user:
        is_pass_correct = check_password_hash(user.password, password)

        if is_pass_correct:
            refresh = create_refresh_token(identity=user.id)
            access = create_access_token(identity=user.id)

            return jsonify({
                'user':{
                    'refresh': refresh,
                    'access': access,
                    'username': user.username,
                    'email': user.email
                }
            }), 201
        
    return jsonify({'error': "Invalid Credentials"}), 401

@auth.get('/me')
def me():
    return "user"