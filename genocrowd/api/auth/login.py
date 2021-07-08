from functools import wraps


from flask import Blueprint, jsonify, make_response, request, session
from flask import current_app as ca

from flask_pymongo import BSONObjectIdConverter

from genocrowd.libgenocrowd.LocalAuth import LocalAuth

from werkzeug.routing import BaseConverter


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


def admin_required(f):
    """Login required function"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        """Login required decorator"""
        if 'user' in session:
            if session['user']['isAdmin']:
                return f(*args, **kwargs)
            return jsonify({"error": True, "errorMessage": "Admin required"})
        return jsonify({"error": True, "errorMessage": "Login required"}), 401

    return decorated_function


@auth_bp.route('/api/auth/signup', methods=["POST"])
def signup():
    """Creates a new user for Genocrowd
    """
    new_user = {}
    local_auth = LocalAuth(ca, session)
    data = request.get_json()
    local_auth.check_inputs(data)
    if not local_auth.get_error():
        # FIXME is it safe to pass role? where does it come from?
        new_user = local_auth.add_user_to_database(data['username'], data['email'], data['password'], data['grade'], data['role'])
        new_user['_id'] = str(new_user['_id'])
        session['user'] = new_user

    return kill_apollo_session(jsonify({
        'error': local_auth.get_error(),
        'errorMessage': local_auth.get_error_message(),
        'user': new_user
    }))


@auth_bp.route('/api/auth/login', methods=['POST'])
def login():
    """Allows a user to log in on Genocrowd

    Returns
    -------

    user info in json format
    """
    data = request.get_json()
    local_auth = LocalAuth(ca, session)
    result = local_auth.authenticate_user(data)
    if result["user"] != {}:
        if result["user"]['blocked']:
            result = {
                'error': True,
                'errorMessage': ["Your account is blocked"],
                'user': {}}
        else:
            session['user'] = result['user']

    return kill_apollo_session(result)


@auth_bp.route('/api/auth/check', methods=['POST'])
@login_required
def is_user_logged_in():
    """Checks if a user is logged in

    Returns
    -------

    user data in session in json format
    """
    return session['user']


@auth_bp.route('/api/auth/logout', methods=['GET'])
@login_required
def logout():
    """ Logs the user out

    Returns
    -------
    json
        user : empty dictionnary
        logged: False
    """
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
    return kill_apollo_session(result)


@auth_bp.route('/api/auth/password', methods=['POST'])
@login_required
def update_password():
    """Update user password

    Returns
    -------
    json
        The updated user
    """
    data = request.get_json()

    online_user = session['user']
    local_auth = LocalAuth(ca, session)
    result = local_auth.update_password(data, online_user)
    if '_id' in result['user']:
        result['user']['_id'] = str(result['user']['_id'])
        session['user'] = result['user']
    return result


@auth_bp.route('/api/auth/levelup', methods=['POST'])
@login_required
def user_level_up():
    data = request.get_json()
    local_auth = LocalAuth(ca, session)
    result = local_auth.user_level_up(data['annotator'])

    return result


@auth_bp.route('/api/auth/delete', methods=['GET'])
@login_required
def delete_account():
    """ Delete the user account and logs him out
    Returns
    -------
    json
        user : empty dictionnary
        logged: False
    """
    users = ca.mongo.db.users
    bson = BSONObjectIdConverter(BaseConverter)
    users.find_one_and_delete({'_id': bson.to_python(session['user']['_id'])})
    session.pop('user', None)
    ca.logger.debug(session)

    return {'user': {}, 'logged': False}


def kill_apollo_session(content):
    """
    Unset the cookie used by Apollo for authentication.
    Need to use it when the logged user changes (or logs out)
    """
    resp = make_response(content)
    resp.set_cookie('JSESSIONID', '', expires=0)
    return resp
