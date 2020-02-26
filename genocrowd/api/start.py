import git
import sys
import traceback


from flask import (Blueprint, current_app, jsonify, session)

from pkg_resources import get_distribution


start_bp = Blueprint('start', __name__, url_prefix='/')


@start_bp.route('/api/hello', methods=['GET'])
def hello():
    """Dummy routes

    Returns
    -------
    json
        error: True if error, else False
        errorMessage: the error message of error, else an empty string
        message: a welcome message
    """
    try:
        message = "Welcome to Genocrowd" if 'user' not in session else "Hello %s, Welcome to Genocrowd!" % session["user"]["username"]

    except Exception as e:
        traceback.print_exc(file=sys.stdout)
        return jsonify({
            'error': True,
            'errorMessage': str(e),
            'message': ''
        }), 500

    return jsonify({
        'error': False,
        'errorMessage': '',
        'message': message
    })


@start_bp.route('/api/start', methods=['GET'])
def start():
    """Starting route

    Returns
    -------
    json
        Information about a eventualy logged user, and the Genocrowd version
        and a footer message
    """
    try:
        # session.clear()
        if 'user' in session:
            user = session['user']
            logged = True
        else:
            user = {}
            logged = False
        # Get commmit hash
        sha = None
        if current_app.iniconfig.getboolean('genocrowd', 'display_commit_hash'):
            try:
                repo = git.Repo(search_parent_directories=True)
                sha = repo.head.object.hexsha[:10]
            except Exception:
                pass

        # get proxy path
        proxy_path = "/"
        try:
            proxy_path = current_app.iniconfig.get("genocrowd", "reverse_proxy_path")
        except Exception:
            pass

        config = {
            "footerMessage": current_app.iniconfig.get('genocrowd', 'footer_message'),
            "version": get_distribution('genocrowd').version,
            "commit": sha,
            "gitUrl": current_app.iniconfig.get('genocrowd', 'github'),
            "proxyPath": proxy_path,
            "user": user,
            "logged": logged
        }

        json = {
            "error": False,
            "errorMessage": '',
            "config": config
        }

        return jsonify(json)

    except Exception as e:
        traceback.print_exc(file=sys.stdout)
        return jsonify({
            "error": True,
            "errorMessage": str(e),
            "config": {}
        }), 500
