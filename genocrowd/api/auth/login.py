

from functools import wraps
from flask import current_app as ca
from flask import Blueprint, request, json, jsonify, flash, session
from datetime import datetime
from flask_pymongo import PyMongo

def login_required(f):
    """Login required function"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        """Login required decorator"""
        print(session)
        if 'user' in session:
            print('okok')
            if not session['user']['blocked']:
                return f(*args, **kwargs)
            return jsonify({"error": True, "errorMessage": "Blocked account"})
        return jsonify({"error": True, "errorMessage": "Login required"}), 401

    return decorated_function

auth_bp = Blueprint('auth', __name__, url_prefix='/')
@auth_bp.route('/api/auth/signup', methods=["POST"])
def signup():
    
    users = ca.mongo.db.users 
    # print('users: ' + str(list(app.mongo.db.users)))
    username = request.get_json()['username']
    email = request.get_json()['email']
    password = ca.bcrypt.generate_password_hash(request.get_json()['password']).decode('utf-8')
    created = datetime.utcnow()

    user_id = users.insert({
        
        'username' : username,
        'email': email,
        'password': password,
        'created': created, 
        'isAdmin': False,
        'isExternal': False
        
    })

    new_user = users.find_one({'_id': user_id})
    print(new_user)
    session['user'] = str(user_id)
    print(user_id)
    result = {'email': new_user['email'] + ' registered'}
    
    return jsonify({'result' : result})

@auth_bp.route('/api/auth/login', methods=['POST'])
def login():
    print('LOGIN')
    users = ca.mongo.db.users 
    email = request.get_json()['email']
    password = request.get_json()['password']
    user = {}
    error_message = ''
    session.clear()
    
    response = users.find_one({'email': email})
    if response:
        if ca.bcrypt.check_password_hash(response['password'], password):
            error = False
            response['_id'] = str(response['_id'])
            session['user'] = response
            
            user = response
            
            
        else:
            error = True
            error_message = "Invalid password"
    else:
        error = True
        error_message = "User not found"
   
    return {'error': error, 'errorMessage': error_message, 'user': user} 
    
@auth_bp.route('/api/auth/jeanbon', methods=['GET'])
@login_required
def is_user_logged_in():
    return 


@auth_bp.route('/api/auth/logout', methods=['POST'])
@login_required
def logout():
    session.pop('user', None)

    ca.logger.debug(session)
    return jsonify({'user': {}, 'logged': False})


