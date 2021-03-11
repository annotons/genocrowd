"""Genocrowd app

Attributes
----------
BLUEPRINTS : Tuple
    Flask blueprints
"""

import configparser

# from celery import Celery

from flask import Flask


from flask_bcrypt import Bcrypt

from flask_ini import FlaskIni

from flask_pymongo import PyMongo

from flask_reverse_proxy_fix.middleware import ReverseProxyPrefixFix

from genocrowd.api.admin.admin import admin_bp
from genocrowd.api.apollo.apollo import apollo_bp
from genocrowd.api.auth.login import auth_bp
from genocrowd.api.data.data import data_bp
from genocrowd.api.start import start_bp
from genocrowd.api.view import view_bp
from genocrowd.libgenocrowd.LocalAuth import LocalAuth


# from kombu import Exchange, Queue

from pkg_resources import get_distribution

import sentry_sdk
from sentry_sdk.integrations.celery import CeleryIntegration
from sentry_sdk.integrations.flask import FlaskIntegration


__all__ = ('create_app')

BLUEPRINTS = (
    start_bp,
    view_bp,
    auth_bp,
    admin_bp,
    data_bp,
    apollo_bp,
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
    app.iniconfig = FlaskIni()
    with app.app_context():
        app.iniconfig.read(config)
        proxy_path = None
        try:
            proxy_path = app.iniconfig.get('genocrowd', 'reverse_proxy_path')
            app.config['REVERSE_PROXY_PATH'] = proxy_path
        except Exception:
            pass
        mongo_dbname = app.iniconfig.get('flask', 'mongo_dbname')
        app.config['MONGO_DBNAME'] = mongo_dbname
        mongo_uri = app.iniconfig.get('flask', 'mongo_uri')
        app.config['MONGO_URI'] = mongo_uri
        if not mongo_uri:
            raise Exception("Missing mongo_uri in config file")
        if not mongo_dbname:
            raise Exception("Missing mongo_dbname in config file")
        app.mongo = PyMongo(app)
        app.bcrypt = Bcrypt(app)
        users = app.mongo.db.users
        app.mongo.db.genes
        app.mongo.db.answers

        app.apollo_admin_email = app.iniconfig.get('genocrowd', 'apollo_admin_email')
        app.apollo_admin_password = app.iniconfig.get('genocrowd', 'apollo_admin_password')
        app.apollo_dataset_path = app.iniconfig.get('genocrowd', 'apollo_dataset_path')
        app.apollo_org_id = app.iniconfig.get('genocrowd', 'apollo_org_id')
        app.apollo_url = app.iniconfig.get('genocrowd', 'apollo_url')
        # We don't want ending slash
        if app.apollo_url.endswith("/"):
            app.apollo_url = app.apollo_url[:-1]

        app.apollo_url_ext = app.iniconfig.get('genocrowd', 'apollo_url_ext')
        # We don't want ending slash
        if app.apollo_url_ext.endswith("/"):
            app.apollo_url_ext = app.apollo_url_ext[:-1]

        configure_logging(app)

        if users.find_one() is None:
            # Create default admin user
            # FIXME wait for apollo to be ready?
            local_auth = LocalAuth(app, None)
            local_auth.add_user_to_database('admin', app.apollo_admin_email, app.apollo_admin_password, 'admin')

        if blueprints is None:
            blueprints = BLUEPRINTS

        for blueprint in blueprints:
            app.register_blueprint(blueprint)

    if proxy_path:
        ReverseProxyPrefixFix(app)
    return app


def configure_logging(app):
    """Configure logging."""

    import logging

    # Set log level
    app.logger.setLevel(logging.INFO)


# def create_celery(app):
#     """Create the celery object

#     Parameters
#     ----------
#     app : Flask
#         Genocrowd Flask application

#     Returns
#     -------
#     Celery
#         Celery object
#     """
#     celery = Celery(app.import_name, backend=app.iniconfig.get(
#         "celery", "result_backend"), broker=app.iniconfig.get("celery", "broker_url"))
#     # celery.conf.update(app.config)
#     task_base = celery.Task

#     default_exchange = Exchange('default', type='direct')

#     celery.conf.task_queues = (
#         Queue('default', default_exchange, routing_key='default'),
#     )
#     celery.conf.task_default_queue = 'default'

#     class ContextTask(task_base):
#         abstract = True

#         def __call__(self, *args, **kwargs):
#             with app.app_context():
#                 return task_base.__call__(self, *args, **kwargs)
#     celery.Task = ContextTask

#     app.celery = celery
#     return celery
