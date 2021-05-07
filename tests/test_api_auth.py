from . import GenocrowdTestCase


class TestApiAuth(GenocrowdTestCase):
    """Test AskOmics API /api/auth/<something>"""

    def test_signup_ok(self, client):
        ok_data = {
            "username": "jwick",
            "password": "dontkillmydog",
            "passwordconf": "dontkillmydog",
            "email": "jwick@genocrowd.org",
            "grade": "mygrade",
            "role": 'user',
            "total_annotation": 0
        }

        response = client.client.post('/api/auth/signup', json=ok_data)
        assert response.status_code == 200
        assert response.json['error'] is False
        assert response.json['errorMessage'] == []
        assert response.json['user'] != {} and '_id' in response.json['user'] != {}

        # Test logged
        with client.client.session_transaction() as sess:
            assert 'user' in sess
            assert sess["user"]['username'] == "jwick" and sess["user"]['email'] == "jwick@genocrowd.org"

    def test_signup_duplicate(self, client):
        ok_data = {
            "username": "jwick",
            "password": "dontkillmydog",
            "passwordconf": "dontkillmydog",
            "email": "jwick@genocrowd.org",
            "grade": "mygrade",
            "role": 'user'
        }

        response = client.client.post('/api/auth/signup', json=ok_data)
        assert response.status_code == 200
        assert response.json['error'] is False
        assert response.json['errorMessage'] == []
        assert response.json['user'] != {} and '_id' in response.json['user'] != {}

        # Test logged
        with client.client.session_transaction() as sess:
            assert 'user' in sess
            assert sess["user"]['username'] == "jwick" and sess["user"]['email'] == "jwick@genocrowd.org"

        # Re-insert same user
        response = client.client.post('/api/auth/signup', json=ok_data)
        assert response.status_code == 200
        assert response.json == {
            'error': True,
            'errorMessage': ["Username already registered", "Email already registered"],
            'user': {}
        }

    def test_signup_empty(self, client):

        empty_username_data = {
            "username": "",
            "password": "dontkillmydog",
            "passwordconf": "dontkillmydog",
            "email": "jwick@genocrowd.org",
            "grade": "mygrade",
            "role": 'user'
        }

        # username empty
        response = client.client.post('/api/auth/signup', json=empty_username_data)
        assert response.status_code == 200
        assert response.json == {
            'error': True,
            'errorMessage': ['Username name empty'],
            'user': {}
        }

    def test_signup_invalid_email(self, client):

        invalid_email_data = {
            "username": "jwick",
            "password": "dontkillmydog",
            "passwordconf": "dontkillmydog",
            "email": "xx",
            "grade": "mygrade",
            "role": 'user'
        }

        # non valid email
        response = client.client.post('/api/auth/signup', json=invalid_email_data)
        assert response.status_code == 200
        assert response.json == {
            'error': True,
            'errorMessage': ['Not a valid email'],
            'user': {}
        }

    def test_signup_bad_passw(self, client):

        diff_password_data = {
            "username": "jwick",
            "password": "dontkillmydog",
            "passwordconf": "dontstealmycar",
            "email": "jwick@genocrowd.org",
            "grade": "mygrade",
            "role": 'user'
        }

        # different password
        response = client.client.post('/api/auth/signup', json=diff_password_data)
        assert response.status_code == 200
        assert response.json == {
            'error': True,
            'errorMessage': ["Password doesn't match"],
            'user': {}
        }

    def test_wrong_login_name(self, client):
        """Test /api/auth/login route with wrong credentials"""
        inputs_wrong_username = {
            "login": "xx",
            "password": "iamjohndoe"
        }

        client.create_two_users()

        response = client.client.post('/api/auth/login', json=inputs_wrong_username)

        assert response.status_code == 200
        assert response.json == {
            'error': True,
            'errorMessage': ["Incorrect login identifier"],
            'user': {}
        }

        # Test logged
        with client.client.session_transaction() as sess:
            assert 'user' not in sess

    def test_wrong_login_email(self, client):
        """Test /api/auth/login route with wrong credentials"""

        inputs_wrong_email = {
            "login": "xx@example.org",
            "password": "iamjohndoe"
        }

        client.create_two_users()

        response = client.client.post('/api/auth/login', json=inputs_wrong_email)

        assert response.status_code == 200
        assert response.json == {
            'error': True,
            'errorMessage': ["Incorrect login identifier"],
            'user': {}
        }

        # Test logged
        with client.client.session_transaction() as sess:
            assert 'user' not in sess

    def test_wrong_login_pass(self, client):
        """Test /api/auth/login route with wrong credentials"""
        inputs_wrong_password = {
            "login": "jdoe@genocrowd.org",
            "password": "xx"
        }

        client.create_two_users()

        response = client.client.post('/api/auth/login', json=inputs_wrong_password)

        assert response.status_code == 200
        assert response.json == {
            'error': True,
            'errorMessage': ["Invalid password"],
            'user': {}
        }

        # Test logged
        with client.client.session_transaction() as sess:
            assert 'user' not in sess

    def test_ok_login(self, client):
        """Test /api/auth/login route with good credentials"""
        ok_inputs_email = {
            "login": "jdoe@genocrowd.org",
            "password": "iamjohndoe"
        }

        ok_inputs_username = {
            "login": "jdoe",
            "password": "iamjohndoe"
        }

        client.create_two_users()

        response = client.client.post('/api/auth/login', json=ok_inputs_username)

        assert response.status_code == 200
        assert response.json["error"] is False
        assert response.json["user"]["username"] == ok_inputs_username["login"]

        response = client.client.post('/api/auth/login', json=ok_inputs_email)

        assert response.status_code == 200
        assert response.json["error"] is False
        assert response.json["user"]['email'] == ok_inputs_email['login']

        # Test logged
        with client.client.session_transaction() as sess:
            assert 'user' in sess
            assert sess["user"]['username'] == "jdoe" and sess["user"]['email'] == "jdoe@genocrowd.org"

    def test_update_profile(self, client):
        """Test /api/auth/profile route"""
        update_all_data = {
            "newUsername": "jdododo",
            "newEmail": "jdododo@genocrowd.org"
        }

        update_username_data = {
            "newUsername": "jdododo",
            "newEmail": ""
        }

        update_email_data = {
            "newUsername": "",
            "newEmail": "jdododo@genocrowd.org"
        }

        update_empty_data = {
            "newUsername": "",
            "newEmail": ""
        }

        client.create_two_users()
        login = client.client.post("/api/auth/login", json={
            "login": "jdoe",
            "password": "iamjohndoe"
        })
        assert login.status_code == 200

        response = client.client.post("/api/auth/profile", json=update_empty_data)
        assert response.status_code == 200
        assert response.json["user"]["username"] == "jdoe"

        # Assert database is untouched
        # TODO:

        # Assert session is untouched
        with client.client.session_transaction() as sess:
            assert 'user' in sess
            assert sess["user"]['username'] == "jdoe" and sess["user"]['email'] == "jdoe@genocrowd.org"

        response = client.client.post("/api/auth/profile", json=update_username_data)
        assert response.status_code == 200
        assert response.json["user"]["username"] == update_username_data["newUsername"]

        # Assert database is updated
        # TODO:

        # Assert session is updated
        with client.client.session_transaction() as sess:
            assert 'user' in sess
            assert sess["user"]['username'] == update_username_data["newUsername"] and sess["user"]['email'] == "jdoe@genocrowd.org"

        response = client.client.post("/api/auth/profile", json=update_email_data)
        assert response.status_code == 200
        assert response.json["user"]["email"] == update_email_data["newEmail"]
        # Assert database is updated
        # TODO:

        # Assert session is updated
        with client.client.session_transaction() as sess:
            assert 'user' in sess
            assert sess["user"]['username'] == "jdododo" and sess["user"]['email'] == update_email_data['newEmail']

        response = client.client.post("/api/auth/profile", json=update_all_data)
        assert response.status_code == 200
        assert response.json["user"]["username"] == update_all_data["newUsername"]
        assert response.json["user"]["email"] == update_all_data["newEmail"]

        # Assert database is updated
        # TODO:

        # Assert session is updated
        with client.client.session_transaction() as sess:
            assert 'user' in sess
            assert sess["user"]['username'] == update_all_data["newUsername"] and sess["user"]['email'] == update_all_data["newEmail"]

    def test_update_password_ok(self, client):
        """test /api/auth/password"""

        ok_data = {
            "newPassword": "helloworld",
            "confPassword": "helloworld",
            "oldPassword": "iamjohndoe"
        }

        client.create_two_users()
        client.log_user("jdoe")

        response = client.client.post('/api/auth/password', json=ok_data)
        assert response.status_code == 200
        assert response.json["error"] is False
        assert response.json["user"]["username"] == "jdoe"

    def test_update_password_empty(self, client):
        """test /api/auth/password"""
        empty_data = {
            "newPassword": "",
            "confPassword": "",
            "oldPassword": "iamjohndoe"
        }

        client.create_two_users()
        client.log_user("jdoe")

        response = client.client.post('/api/auth/password', json=empty_data)
        assert response.status_code == 200
        assert response.json["error"] is True
        assert response.json["user"]["username"] == "jdoe"
        assert response.json["user"]["password"] != empty_data["newPassword"]

    def test_update_password_bad(self, client):
        """test /api/auth/password"""
        unidentical_passwords_data = {
            "newPassword": "helloworld",
            "confPassword": "holamundo",
            "oldPassword": "iamjohndoe"
        }

        client.create_two_users()
        client.log_user("jdoe")

        response = client.client.post('/api/auth/password', json=unidentical_passwords_data)
        assert response.status_code == 200
        assert response.json["error"] is True
        assert response.json["user"]["username"] == "jdoe"
        assert response.json["user"]["password"] != unidentical_passwords_data['newPassword']

    def test_logout(self, client):
        """test /api/auth/logout route"""
        client.create_two_users()
        client.log_user("jdoe")

        response = client.client.get('/api/auth/logout')

        assert response.status_code == 200
        assert response.json == {
            "user": {},
            "logged": False
        }
