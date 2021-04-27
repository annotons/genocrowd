from . import GenocrowdTestCase


class TestApiData(GenocrowdTestCase):

    def test_update_groupsAmount_ok(self, client):
        client.create_two_users()
        client.log_user("jdoe")
        ok_data = {
            "newNumber": 2
        }
        response = client.client.post('api/data/setgroupsamount', json=ok_data)
        assert response.status_code == 200
        assert response.json["error"] is False
        assert response.json["groupsAmount"]["updatedExisting"] is True
