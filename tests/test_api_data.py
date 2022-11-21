from . import GenocrowdTestCase


class TestApiData(GenocrowdTestCase):
    """Test AskOmics API /api/data/<something>"""

    def test_update_groups_amount_ok(self, client):
        client.create_two_users()
        client.log_user("jdoe")
        ok_data = {
            "newNumber": 2
        }
        """Test update number of groups"""
        response = client.client.post('api/data/setgroupsamount', json=ok_data)
        assert response.status_code == 200
        assert response.json["error"] is False
        assert response.json["groupsAmount"]["updatedExisting"] is True

        """Test creation group"""
        response2 = client.client.get('/api/admin/getgroups')
        assert len(response2.json["groups"]) == ok_data["newNumber"]

    def test_group_assignement(self, client):
        client.create_two_users()
        client.log_user("jdoe")
        ok_data = {
            "groupsAmount": 2
        }

        response = client.client.post('/api/admin/setgroup', json=ok_data)
        response2 = client.client.get('/api/admin/getusers')
        response3 = client.client.get('/api/admin/getgroups')
        assert response.status_code == 200 and response2.status_code == 200 and response3.status_code == 200
        assert response.json["error"] is False and response2.json["error"] is False and response3.json["error"] is False
        """Test user in the correct group
            test if jsmith group is group 1 and
            test if jsmith is the first student in group 1 list"""
        assert len(response2.json["users"]) == 2
        assert "group" in response2.json["users"][1]
        assert response2.json["users"][1]["group"] == 1
        assert response2.json["users"][1]["_id"] == response3.json["groups"][0]["student"][0]["_id"]
