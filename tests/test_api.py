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
