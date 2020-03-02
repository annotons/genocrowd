from . import GenocrowdTestCase


class TestApiAuth(GenocrowdTestCase):
    """Test AskOmics API /api/auth/<something>"""

    def test_signup(self, client):
        """Test /api/auth/signup route"""
        ok_data = {
            "username": "jwick",
            "password": "dontkillmydog",
            "passwordconf": "dontkillmydog",
            "email": "jwick@.org",
        }

        empty_username_data = {
            "username": "",
            "password": "dontkillmydog",
            "passwordconf": "dontkillmydog",
            "email": "jwick@genocrowd.org"
        }

        unvalid_email_data = {
            "username": "jwick",
            "password": "dontkillmydog",
            "passwordconf": "dontkillmydog",
            "email": "xx"
        }

        diff_password_data = {
            "username": "jwick",
            "password": "dontkillmydog",
            "passwordconf": "dontstealmycar",
            "email": "jwick@genocrowd.org"
        }

        # username empty
        response = client.client.post('/api/auth/signup', json=empty_username_data)
        assert response.status_code == 200
        assert response.json == {
            'error': True,
            'errorMessage': ['Username name empty'],
            'user': {}
        }

        # non valid email
        response = client.client.post('/api/auth/signup', json=unvalid_email_data)
        assert response.status_code == 200
        assert response.json == {
            'error': True,
            'errorMessage': ['Not a valid email'],
            'user': {}
        }

        # different password
        response = client.client.post('/api/auth/signup', json=diff_password_data)
        assert response.status_code == 200
        assert response.json == {
            'error': True,
            'errorMessage': ["Password doesn't match"],
            'user': {}
        }

        # ok inputs
        response = client.client.post('/api/auth/signup', json=ok_data)
        assert response.status_code == 200
        assert response.json == {
            'error': False,
            'errorMessage': [],
            'user': {
                'id': 1,
                'username': "jwick",
                'email': "jwick@genocrowd.org",
                'admin': True,
                'blocked': False,
            }
        }

        # Test logged
        with client.client.session_transaction() as sess:
            assert 'user' in sess
            assert sess["user"] == {
                'id': 1,
                'username': "jwick",
                'email': "jwick@genocrowd.org",
                'admin': True,
                'blocked': False,
            }

        # Re-insert same user
        response = client.client.post('/api/auth/signup', json=ok_data)
        assert response.status_code == 200
        assert response.json == {
            'error': True,
            'errorMessage': ["Username already registered", "Email already registered"],
            'user': {}
        }

    def test_wrong_login(self, client):
        """Test /api/auth/login route with wrong credentials"""
        inputs_wrong_username = {
            "login": "xx",
            "password": "iamjohndoe"
        }

        inputs_wrong_email = {
            "login": "xx@example.org",
            "password": "iamjohndoe"
        }

        inputs_wrong_password = {
            "login": "jdoe@genocrowd.org",
            "password": "xx"
        }

        client.create_two_users()

        response = client.client.post('/api/auth/login', json=inputs_wrong_username)

        assert response.status_code == 200
        assert response.json == {
            'error': True,
            'errorMessage': ["Incorrect login identifier"],
            'user': {}
        }

        response = client.client.post('/api/auth/login', json=inputs_wrong_email)

        assert response.status_code == 200
        assert response.json == {
            'error': True,
            'errorMessage': ["Incorrect login identifier"],
            'user': {}
        }

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
        assert response.json == {
            'error': False,
            'errorMessage': [],
            'user': {
                'fname': "John",
                'lname': "Doe",
                'username': "jdoe",
                'email': "jdoe@genocrowd.org",
                'isAdmin': True,
                'blocked': False,
            }
        }

        response = client.client.post('/api/auth/login', json=ok_inputs_email)

        assert response.status_code == 200
        assert response.json == {
            'error': False,
            'errorMessage': [],
            'user': {
                'username': "jdoe",
                'email': "jdoe@genocrowd.org",
                'isAdmin': True,
                'blocked': False,
            }
        }

        # Test logged
        with client.client.session_transaction() as sess:
            assert 'user' in sess
            assert sess["user"] == {
                'username': "jdoe",
                'email': "jdoe@genocrowd.org",
                'isAdmin': True,
                'blocked': False,
            }

    def test_update_profile(self, client):
        """Test /api/auth/profile route"""
        update_all_data = {
            "newFname": "Johnny",
            "newLname": "Dododo",
            "newEmail": "jdododo@genocrowd.org"
        }

        update_lname_data = {
            "newFname": "",
            "newLname": "Dodo",
            "newEmail": ""
        }

        update_email_data = {
            "newFname": "",
            "newLname": "",
            "newEmail": "jdodo@genocrowd.org"
        }

        update_empty_data = {
            "newFname": "",
            "newLname": "",
            "newEmail": ""
        }

        client.create_two_users()
        client.log_user("jdoe")

        response = client.client.post("/api/auth/profile", json=update_empty_data)
        assert response.status_code == 200
        assert response.json == {
            "error": False,
            "errorMessage": '',
            "user": {
                'id': 1,
                'ldap': False,
                'fname': "John",
                'lname': "Doe",
                'username': "jdoe",
                'email': "jdoe@genocrowd.org",
                'admin': True,
                'blocked': False,
                'quota': 0,
                'apikey': "0000000001",
                'galaxy': {"url": "http://localhost:8081", "apikey": "admin"}
            }
        }
        # Assert database is untouched
        # TODO:

        # Assert session is untouched
        with client.client.session_transaction() as sess:
            assert 'user' in sess
            assert sess["user"] == {
                'id': 1,
                'ldap': False,
                'fname': "John",
                'lname': "Doe",
                'username': "jdoe",
                'email': "jdoe@genocrowd.org",
                'admin': True,
                'blocked': False,
                'quota': 0,
                'apikey': "0000000001",
                'galaxy': {"url": "http://localhost:8081", "apikey": "admin"}
            }

        response = client.client.post("/api/auth/profile", json=update_lname_data)
        assert response.status_code == 200
        assert response.json == {
            "error": False,
            "errorMessage": '',
            "user": {
                'id': 1,
                'ldap': False,
                'fname': "John",
                'lname': "Dodo",
                'username': "jdoe",
                'email': "jdoe@genocrowd.org",
                'admin': True,
                'blocked': False,
                'quota': 0,
                'apikey': "0000000001",
                'galaxy': {"url": "http://localhost:8081", "apikey": "admin"}
            }
        }
        # Assert database is updated
        # TODO:

        # Assert session is updated
        with client.client.session_transaction() as sess:
            assert 'user' in sess
            assert sess["user"] == {
                'id': 1,
                'ldap': False,
                'fname': "John",
                'lname': "Dodo",
                'username': "jdoe",
                'email': "jdoe@genocrowd.org",
                'admin': True,
                'blocked': False,
                'quota': 0,
                'apikey': "0000000001",
                'galaxy': {"url": "http://localhost:8081", "apikey": "admin"}
            }

        response = client.client.post("/api/auth/profile", json=update_email_data)
        assert response.status_code == 200
        assert response.json == {
            "error": False,
            "errorMessage": '',
            "user": {
                'id': 1,
                'ldap': False,
                'fname': "John",
                'lname': "Dodo",
                'username': "jdoe",
                'email': "jdodo@genocrowd.org",
                'admin': True,
                'blocked': False,
                'quota': 0,
                'apikey': "0000000001",
                'galaxy': {"url": "http://localhost:8081", "apikey": "admin"}
            }
        }
        # Assert database is updated
        # TODO:

        # Assert session is updated
        with client.client.session_transaction() as sess:
            assert 'user' in sess
            assert sess["user"] == {
                'id': 1,
                'ldap': False,
                'fname': "John",
                'lname': "Dodo",
                'username': "jdoe",
                'email': "jdodo@genocrowd.org",
                'admin': True,
                'blocked': False,
                'quota': 0,
                'apikey': "0000000001",
                'galaxy': {"url": "http://localhost:8081", "apikey": "admin"}
            }

        response = client.client.post("/api/auth/profile", json=update_all_data)
        assert response.status_code == 200
        assert response.json == {
            "error": False,
            "errorMessage": '',
            "user": {
                'id': 1,
                'ldap': False,
                'fname': "Johnny",
                'lname': "Dododo",
                'username': "jdoe",
                'email': "jdododo@genocrowd.org",
                'admin': True,
                'blocked': False,
                'quota': 0,
                'apikey': "0000000001",
                'galaxy': {"url": "http://localhost:8081", "apikey": "admin"}
            }
        }
        # Assert database is updated
        # TODO:

        # Assert session is updated
        with client.client.session_transaction() as sess:
            assert 'user' in sess
            assert sess["user"] == {
                'id': 1,
                'ldap': False,
                'fname': "Johnny",
                'lname': "Dododo",
                'username': "jdoe",
                'email': "jdododo@genocrowd.org",
                'admin': True,
                'blocked': False,
                'quota': 0,
                'apikey': "0000000001",
                'galaxy': {"url": "http://localhost:8081", "apikey": "admin"}
            }

    def test_update_password(self, client):
        """test /api/auth/password"""
        empty_data = {
            "newPassword": "",
            "confPassword": "",
            "oldPassword": ""
        }

        unidentical_passwords_data = {
            "newPassword": "helloworld",
            "confPassword": "holamundo",
            "oldPassword": "iamjohndoe"
        }

        wrong_old_passwords_data = {
            "newPassword": "helloworld",
            "confPassword": "helloworld",
            "oldPassword": "wrongpassword"
        }

        ok_data = {
            "newPassword": "helloworld",
            "confPassword": "helloworld",
            "oldPassword": "iamjohndoe"
        }

        client.create_two_users()
        client.log_user("jdoe")

        response = client.client.post('/api/auth/password', json=empty_data)
        assert response.status_code == 200
        assert response.json == {
            "error": True,
            "errorMessage": 'Empty password',
            "user": {
                'id': 1,
                'ldap': False,
                'fname': "John",
                'lname': "Doe",
                'username': "jdoe",
                'email': "jdoe@genocrowd.org",
                'admin': True,
                'blocked': False,
                'quota': 0,
                'apikey': "0000000001",
                'galaxy': {"url": "http://localhost:8081", "apikey": "admin"}
            }
        }

        response = client.client.post('/api/auth/password', json=unidentical_passwords_data)
        assert response.status_code == 200
        assert response.json == {
            "error": True,
            "errorMessage": 'New passwords are not identical',
            "user": {
                'id': 1,
                'ldap': False,
                'fname': "John",
                'lname': "Doe",
                'username': "jdoe",
                'email': "jdoe@genocrowd.org",
                'admin': True,
                'blocked': False,
                'quota': 0,
                'apikey': "0000000001",
                'galaxy': {"url": "http://localhost:8081", "apikey": "admin"}
            }
        }

        response = client.client.post('/api/auth/password', json=wrong_old_passwords_data)
        assert response.status_code == 200
        assert response.json == {
            "error": True,
            "errorMessage": 'Incorrect old password',
            "user": {
                'id': 1,
                'ldap': False,
                'fname': "John",
                'lname': "Doe",
                'username': "jdoe",
                'email': "jdoe@genocrowd.org",
                'admin': True,
                'blocked': False,
                'quota': 0,
                'apikey': "0000000001",
                'galaxy': {"url": "http://localhost:8081", "apikey": "admin"}
            }
        }

        response = client.client.post('/api/auth/password', json=ok_data)
        assert response.status_code == 200
        assert response.json == {
            "error": False,
            "errorMessage": '',
            "user": {
                'id': 1,
                'ldap': False,
                'fname': "John",
                'lname': "Doe",
                'username': "jdoe",
                'email': "jdoe@genocrowd.org",
                'admin': True,
                'blocked': False,
                'quota': 0,
                'apikey': "0000000001",
                'galaxy': {"url": "http://localhost:8081", "apikey": "admin"}
            }
        }

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
