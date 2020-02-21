

from functools import wraps
from flask import current_app as ca
from flask import Blueprint, request, json, jsonify, flash, session
from datetime import datetime

from genocrowd.libgenocrowd.LocalAuth import LocalAuth


auth_bp = Blueprint('auth', __name__, url_prefix='/')


def login_required(f):
    """Login required function"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        """Login required decorator""" 
        if 'user' in session:
            if not session['user']['blocked']:
                return f(*args, **kwargs)
            return jsonify({"error": True, "errorMessage": "Blocked account"})
        return jsonify({"error": True, "errorMessage": "Login required"}), 401

    return decorated_function


@auth_bp.route('/api/auth/signup', methods=["POST"])
def signup():
    error = False
    error_message = ''
    users = ca.mongo.db.users
    # print('users: ' + str(list(app.mongo.db.users)))
    username = request.get_json()['username']
    email = request.get_json()['email']
    password = ca.bcrypt.generate_password_hash(
        request.get_json()['password']).decode('utf-8')
    created = datetime.utcnow()

    user_id = users.insert({
        'username': username,
        'email': email,
        'password': password,
        'created': created,
        'isAdmin': False,
        'isExternal': False,
        'blocked': False
    })

    new_user = users.find_one({'_id': user_id})
    new_user['_id'] = str(new_user['_id'])
    session['user'] = new_user
    return jsonify({
        'error': error,
        'errorMessage': error_message,
        'user': new_user
    })


@auth_bp.route('/api/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    local_auth = LocalAuth(ca, session)
    result = local_auth.authenticate_user(data)
    session['user'] = result['user']
    return result


@auth_bp.route('/api/auth/check', methods=['POST'])
@login_required
def is_user_logged_in():
    return session['user']


@auth_bp.route('/api/auth/logout', methods=['GET'])
@login_required
def logout():
    session.pop('user', None)

    ca.logger.debug(session)
    return jsonify({'user': {}, 'logged': False})


@auth_bp.route('/api/auth/profile', methods=['POST'])
@login_required
def update_profile():
    """Update user profile (names and email)

    Returns
    -------
    json
        The updated user
    """
    data = request.get_json()
    online_user = session['user']
    local_auth = LocalAuth(ca, session)
    result = local_auth.update_profile(data, online_user)
    result['user']['_id'] = str(result['user']['_id'])
    session['user'] = result['user']
    return result
