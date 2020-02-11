#recup objet mongo
from flask import current_app as ca
from flask import Blueprint, request, json, jsonify, flash
from datetime import datetime
from flask_jwt_extended import JWTManager 
from flask_jwt_extended import create_access_token


auth_bp = Blueprint('auth', __name__, url_prefix='/')
@auth_bp.route('/api/auth/signup', methods=["POST"])
def signup():
    
    users = ca.mongo.db.users 
    username = request.get_json()['username']
    email = request.get_json()['email']
    password = ca.bcrypt.generate_password_hash(request.get_json()['password']).decode('utf-8')
    created = datetime.utcnow()

    user_id = users.insert({
        'first_name': first_name,
        'last_name': last_name,
        'username' : username,
        'email': email,
        'password': password,
        'created': created 
    })

    new_user = users.find_one({'_id': user_id})

    result = {'email': new_user['email'] + ' registered'}
    
    return jsonify({'result' : result})

@auth_bp.route('/api/auth/login', methods=['POST'])
def login():
    users = ca.mongo.db.users 
    email = request.get_json()['email']
    password = request.get_json()['password']
    result = ""

    response = users.find_one({'email': email})

    if response:
        if ca.bcrypt.check_password_hash(response['password'], password):
            access_token = create_access_token(identity = {
                'first_name': response['first_name'],
                'last_name': response['last_name'],
                'email': response['email']
            })
            result = jsonify({'token':access_token})
        else:
            result = jsonify({"error":"Invalid username and password"})
    else:
        result = jsonify({"result":"No results found"})
   
    return result 

@auth_bp.route('/update', methods=['POST'])
def update_user():
    return ''


