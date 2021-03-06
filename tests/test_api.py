from pkg_resources import get_distribution

from . import GenocrowdTestCase


class TestApi(GenocrowdTestCase):
    """Test Genocrowd API"""

    def test_hello(self, client):
        """Test /api/hello route"""
        response = client.client.get('/api/hello')

        assert response.status_code == 200
        assert response.json == {
            "error": False,
            "errorMessage": '',
            "message": "Welcome to Genocrowd"
        }

    def test_start_anonymous(self, client):
        """Test /api/start route"""
        # Non logged
        expected_config_nouser = {
            'footerMessage': client.get_config('genocrowd', 'footer_message'),
            "version": get_distribution('genocrowd').version,
            "commit": None,
            "gitUrl": "https://github.com/annotons/genocrowd",
            "proxyPath": "/",
            "user": {},
            "logged": False
        }
        response = client.client.get('/api/start')
        assert response.status_code == 200
        assert response.json == {
            "error": False,
            "errorMessage": '',
            "config": expected_config_nouser
        }

    def test_start_admin(self, client):

        # Create database and user
        client.create_two_users()

        # Jdoe (admin) logged
        client.log_user("jdoe")

        response = client.client.get('/api/start')

        expected_config_jdoe = {
            'footerMessage': client.get_config('genocrowd', 'footer_message'),
            "version": get_distribution('genocrowd').version,
            "commit": None,
            "gitUrl": "https://github.com/annotons/genocrowd",
            "proxyPath": "/",
            "user": {},
            "logged": False
        }
        expected_config_jdoe['logged'] = True
        expected_config_jdoe["user"] = {
            '_id': response.json['config']['user']['_id'],
            'username': "jdoe",
            "password": response.json['config']['user']['password'],
            'email': "jdoe@genocrowd.org",
            'isAdmin': True,
            'blocked': False,
            'isExternal': False,
            'created': response.json["config"]["user"]["created"],
            'grade': "ADMIN",
            'group': None,
            'role': 'admin'

        }

        assert response.status_code == 200
        assert response.json == {
            "error": False,
            "errorMessage": '',
            "config": expected_config_jdoe
        }

    def test_start_user(self, client):

        # Create database and user
        client.create_two_users()

        # jsmith (non admin) logged
        client.log_user("jsmith")

        response = client.client.get('/api/start')

        expected_config_jsmith = {
            'footerMessage': client.get_config('genocrowd', 'footer_message'),
            "version": get_distribution('genocrowd').version,
            "commit": None,
            "gitUrl": "https://github.com/annotons/genocrowd",
            "proxyPath": "/",
            "user": {},
            "logged": False
        }
        expected_config_jsmith["logged"] = True
        expected_config_jsmith["user"] = {
            '_id': response.json['config']['user']['_id'],
            'username': "jsmith",
            "password": response.json['config']['user']['password'],
            'email': "jsmith@genocrowd.org",
            'isAdmin': False,
            'blocked': False,
            'isExternal': False,
            'created': response.json["config"]["user"]["created"],
            'grade': "mygrade",
            'group': None,
            'role': 'user'
        }

        assert response.status_code == 200
        assert response.json == {
            "error": False,
            "errorMessage": '',
            "config": expected_config_jsmith
        }
