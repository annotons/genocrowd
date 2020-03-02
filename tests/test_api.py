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

    def test_start(self, client):
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

        # Create database and user
        client.create_two_users()

        # Jdoe (admin) logged-
        client.log_user("jdoe")

        expected_config_jdoe = expected_config_nouser
        expected_config_jdoe["logged"] = True
        expected_config_jdoe["user"] = {
            'id': 1,
            'username': "jdoe",
            'email': "jdoe@genocrowd.org",
            'admin': True,
            'blocked': False,
        }
        response = client.client.get('/api/start')

        assert response.status_code == 200
        assert response.json == {
            "error": False,
            "errorMessage": '',
            "config": expected_config_jdoe
        }

        # jsmith (non admin) logged
        client.log_user("jsmith")

        expected_config_jsmith = expected_config_nouser
        expected_config_jsmith["logged"] = True
        expected_config_jsmith["user"] = {
            'id': 2,
            'username': "jsmith",
            'email': "jsmith@genocrowd.org",
            'admin': False,
            'blocked': False,
        }
        response = client.client.get('/api/start')

        assert response.status_code == 200
        assert response.json == {
            "error": False,
            "errorMessage": '',
            "config": expected_config_jsmith
        }
