"""conftest"""
import random
from datetime import datetime

from flask_pymongo import BSONObjectIdConverter

from genocrowd.app import create_app
from genocrowd.libgenocrowd.LocalAuth import LocalAuth

import pytest

from werkzeug.routing import BaseConverter


@pytest.fixture
def client():
    """Summary

    Returns
    -------
    TYPE
        Description
    """
    client = Client()

    yield client


class Client(object):
    """Fixture class

    Attributes
    ----------
    app : TYPE
        Description
    client : TYPE
        Description
    config : TYPE
        Description
    ctx : TYPE
        Description
    """

    def __init__(self, config="config/genocrowd.test.ini"):
        """Summary

        Parameters
        ----------
        config : str, optional
            Description
        """
        # Config
        self.config = config

        # create app
        self.app = create_app(config=self.config)
        # context
        self.ctx = self.app.app_context()
        self.ctx.push()

        # Client
        self.client = self.app.test_client()
        self.session = {}

        # bson
        self.bson = BSONObjectIdConverter(BaseConverter)

        self.reset_db()

    def get_config(self, section, entry, boolean=False):
        """Summary

        Parameters
        ----------
        section : TYPE
            Description
        entry : TYPE
            Description
        boolean : bool, optional
            Description

        Returns
        -------
        TYPE
            Description
        """
        if boolean:
            return self.app.iniconfig.getboolean(section, entry)
        return self.app.iniconfig.get(section, entry)

    def get_client(self):
        """Summary

        Returns
        -------
        TYPE
            Description
        """
        return self.client

    def log_user(self, username):
        """Summary

        Parameters
        ----------
        username : TYPE
            Description
        """
        auth = LocalAuth(self.app, self.session)
        user = auth.users.find_one({'username': username})
        with self.client.session_transaction() as sess:
            user['_id'] = str(user['_id'])
            sess["user"] = user
        self.session = sess

    def create_user(self, username):
        """Summary

        Parameters
        ----------
        username : TYPE
            Description

        Returns
        -------
        TYPE
            Description
        """
        uinfo = {
            "username": "jdoe" if username == "jdoe" else "jsmith",
            "password": self.app.bcrypt.generate_password_hash("iamjohndoe").decode('utf-8') if username == "jdoe" else self.app.bcrypt.generate_password_hash("iamjanesmith").decode('utf-8'),
            "email": "jdoe@genocrowd.org" if username == "jdoe" else "jsmith@genocrowd.org",
            "isAdmin": True if username == "jdoe" else False,
            "isExternal": False,
            "created": datetime.utcnow(),
            "blocked": False,
            "grade": "ADMIN" if username == "jdoe" else "mygrade",
            "group": None,
            "role": 'admin' if username == "jdoe" else "user"
        }

        auth = LocalAuth(self.app, self.session)
        auth.users.insert_one(uinfo)
        user = auth.users.find_one({'username': uinfo['username']})
        user['_id'] = str(user['_id'])
        return user

    def create_two_users(self):
        """Create jdoe and jsmith"""
        self.create_user("jdoe")
        self.create_user("jsmith")

    def logout_user(self, username):
        """Summary

        Parameters
        ----------
        username : TYPE
            Description
        """
        self.session.pop('user', None)

    def reset_db(self):
        self.app.mongo.db.users.drop()

    @staticmethod
    def get_random_string(number):
        """return a random string of n character

        Parameters
        ----------
        number : int
            number of character of the random string

        Returns
        -------
        str
            a random string of n chars
        """
        alpabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
        return ''.join(random.choice(alpabet) for i in range(number))
