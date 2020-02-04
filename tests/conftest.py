"""conftest"""
import random

from genocrowd.app import create_app, create_celery

import pytest


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

    # teardown
    client.clean()


class Client(object):
    """Fixtrue class

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
    db_path : TYPE
        Description
    dir_path : TYPE
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
        self.db_path = "{}/database.db".format(self.dir_path)

        # create app
        self.app = create_app(config=self.config)
        create_celery(self.app)
        self.app.iniconfig.set('genocrowd', 'database_path', self.db_path)

        # context
        self.ctx = self.app.app_context()
        self.ctx.push()

        # Client
        self.client = self.app.test_client()
        self.session = {}

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
