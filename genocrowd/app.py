"""Genocrowd app

Attributes
----------
BLUEPRINTS : Tuple
    Flask blueprints
"""

import configparser
from genocrowd.api.auth.login import auth_bp

from genocrowd.api.start import start_bp
from genocrowd.api.view import view_bp


from celery import Celery
from kombu import Exchange, Queue

from flask import Flask

from flask_bcrypt import Bcrypt
from flask_ini import FlaskIni
from flask import session
from flask_reverse_proxy_fix.middleware import ReverseProxyPrefixFix

from pkg_resources import get_distribution
from flask_pymongo import PyMongo
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration
from sentry_sdk.integrations.celery import CeleryIntegration



__all__ = ('create_app', 'create_celery')

BLUEPRINTS = (
    start_bp,
    view_bp,
    auth_bp,
)


def create_app(config='config/genocrowd.ini', app_name='genocrowd', blueprints=None):
    """Create the Genocrowd app

    Parameters
    ----------
    config : str, optional
        Path to the config file
    app_name : str, optional
        Application name
    blueprints : None, optional
        Flask blueprints

    Returns
    -------
    Flask
        Genocrowd Flask application
    """
   
    conf = configparser.ConfigParser()
    conf.read(config)

    sentry_dsn = None
    try:
        sentry_dsn = conf['sentry']['server_dsn']
    except Exception:
        pass

    if sentry_dsn:
        version = get_distribution('genocrowd').version
        name = get_distribution('genocrowd').project_name
        sentry_sdk.init(
            dsn=sentry_dsn,
            release="{}@{}".format(name, version),
            integrations=[FlaskIntegration(), CeleryIntegration()]
        )

    app = Flask(app_name, static_folder='static', template_folder='templates')
    app.config['MONGO_DBNAME'] = 'Genocrowd'
    app.config["MONGO_URI"] = "mongodb://localhost:27017/Genocrowd"
    app.mongo = PyMongo(app)
    app.bcrypt = Bcrypt(app)
    
    app.iniconfig = FlaskIni()
    with app.app_context():
        
        app.iniconfig.read(config)
        proxy_path = None
        try:
            proxy_path = app.iniconfig.get('genocrowd', 'reverse_proxy_path')
            app.config['REVERSE_PROXY_PATH'] = proxy_path
        except Exception:
            pass

        if blueprints is None:
            blueprints = BLUEPRINTS

        for blueprint in blueprints:
            app.register_blueprint(blueprint)

    if proxy_path:
        ReverseProxyPrefixFix(app)
    return app


def create_celery(app):
    """Create the celery object

    Parameters
    ----------
    app : Flask
        Genocrowd Flask application

    Returns
    -------
    Celery
        Celery object
    """
    celery = Celery(app.import_name, backend=app.iniconfig.get("celery", "result_backend"), broker=app.iniconfig.get("celery", "broker_url"))
    # celery.conf.update(app.config)
    task_base = celery.Task

    default_exchange = Exchange('default', type='direct')

    celery.conf.task_queues = (
        Queue('default', default_exchange, routing_key='default'),
    )
    celery.conf.task_default_queue = 'default'

    class ContextTask(task_base):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return task_base.__call__(self, *args, **kwargs)
    celery.Task = ContextTask

    app.celery = celery
    return celery
