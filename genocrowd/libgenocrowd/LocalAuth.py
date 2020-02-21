"""Contain the Database class"""

from genocrowd.libgenocrowd.Params import Params
from genocrowd.libgenocrowd.Utils import Utils

from validate_email import validate_email
from flask_pymongo import BSONObjectIdConverter
from werkzeug.routing import BaseConverter
class LocalAuth(Params):
    """Manage user authentication"""

    def __init__(self, app, session):
        """init

        Parameters
        ----------
        app : Flask
            flask app
        session :
            Genocrowd session, contain the user
        """
        Params.__init__(self, app, session)

    def check_inputs(self, inputs):
        """Check user inputs

        Check if inputs are not empty, if passwords are identical, and if
        username and email are not already in the database

        Parameters
        ----------
        inputs : dict
            User inputs

        """

        if not inputs['username']:
            self.error = True
            self.error_message.append('Username name empty')

        if not validate_email(inputs['email']):
            self.error = True
            self.error_message.append('Not a valid email')

        if not inputs['password']:
            self.error = True
            self.error_message.append('Password empty')

        if inputs['password'] != inputs['passwordconf']:
            self.error = True
            self.error_message.append("Passwords doesn't match")

        if self.is_username_in_db(inputs['username']):
            self.error = True
            self.error_message.append('Username already registered')

        if self.is_email_in_db(inputs['email']):
            self.error = True
            self.error_message.append('Email already registered')

    def is_username_in_db(self, username):
        """
        Check if the username is present in the database

        Parameters
        ----------
        username : str
            Username

        Returns
        -------
        bool
            True if the user exist
        """
        users = self.app.mongo.db.users 
        response = users.find_one({'username': username})
        if response:
            return True
        else:
            return False

    def is_email_in_db(self, email):
        """
        Check if the email is present in the database

        Parameters
        ----------
        email : str
            Email

        Returns
        -------
        bool
            True if the email exist
        """
        users = self.app.mongo.db.users 
        response = users.find_one({'email': email})
        if response:
            return True
        else:
            return False

    def get_number_of_users(self):
        """get the number of users in the DB

        Returns
        -------
        int
            Number of user in the Database
        """
        return self.app.mongo.db.users.count_documents()

    def authenticate_user(self, data):
        """
        check if the password is the good password associated with the email or the username

        Parameters
        ----------
        login: username or email

        Returns
        -------
        dict
            user info if authentication success
        """
        login = data['login']
        password = data['password']
        users = self.app.mongo.db.users
        user = {}
        error_message = ''
        if self.is_username_in_db(login):
            response = users.find_one({'username': login})
            if self.app.bcrypt.check_password_hash(response['password'], password):
                error = False
                response['_id'] = str(response['_id'])
                user = response
            else:
                error = True
                error_message = "Invalid password"

        elif self.is_email_in_db(login):
            response = users.find_one({'email': login})
            if self.app.bcrypt.check_password_hash(response['password'], password):
                error = False
                response['_id'] = str(response['_id'])

                user = response
            else:
                error = True
                error_message = "Invalid password"
        else:
            error = True
            error_message = "User not found"
        return {'error': error, 'errorMessage': error_message, 'user': user}

    def update_profile(self, data, user):
        """Update the profile of a user

        Parameters
        ----------
        inputs : dict
            fields to update
        user : dict
            The current user

        Returns
        -------
        dict
            error, error message and updated user
        """
        users = self.app.mongo.db.users
        print(users)
        error = False
        error_message = ''
        username = data['newUsername']
        email = data['newEmail']
        if len(username) == 0:
            username = user['username']
        if len(email) == 0:
            email = user['email']
        bson = BSONObjectIdConverter(BaseConverter)
        updated_user = users.find_one_and_update({'_id': bson.to_python(user['_id'])}, {'$set': {
                'username': username,
                'email': email
            }})
        print(str(updated_user) + '   UPDATED')
        return {
            'error': error,
            'errorMessage': error_message,
            'user': updated_user
        }

        

    def update_password(self, inputs, user):
        """Update the password of a user

        Parameters
        ----------
        inputs : dict
            Curent password and the new one (and confirmation)
        user : dict
            The current user

        Returns
        -------
        dict
            error, error message and updated user
        """
        error = False
        error_message = ''

        database = Database(self.app, self.session)

        # check if new passwords are identicals
        password_identical = (inputs['newPassword'] == inputs['confPassword'])

        if not inputs["newPassword"] == '':
            if password_identical:
                # Try to authenticate the user with his old password
                credentials = {'login': user['username'], 'password': inputs['oldPassword']}
                authentication = self.authenticate_user(credentials)
                if not authentication['error']:
                    # Update the password
                    salt = Utils.get_random_string(20)
                    salted_pw = self.settings.get('askomics', 'password_salt') + inputs['newPassword'] + salt
                    sha512_pw = hashlib.sha512(salted_pw.encode('utf-8')).hexdigest()

                    query = '''
                    UPDATE users SET
                    password=?, salt=?
                    WHERE username=?
                    '''

                    database.execute_sql_query(query, (sha512_pw, salt, user['username']))
                else:
                    error = True
                    error_message = 'Incorrect old password'
            else:
                error = True
                error_message = 'New passwords are not identical'
        else:
            error = True
            error_message = 'Empty password'

        return {'error': error, 'error_message': error_message, 'user': user}


    def get_all_users(self):
        """Get all user info

        Returns
        -------
        list
            All user info
        """
        database = Database(self.app, self.session)

        query = '''
        SELECT u.user_id, u.ldap, u.fname, u.lname, u.username, u.email, u.admin, u.blocked, u.quota, g.url, g.apikey
        FROM users u
        LEFT JOIN galaxy_accounts g ON u.user_id=g.user_id
        GROUP BY u.user_id
        '''

        rows = database.execute_sql_query(query)

        users = []

        if rows:
            for row in rows:
                user = {}
                user['ldap'] = row[1]
                user['fname'] = row[2]
                user['lname'] = row[3]
                user['username'] = row[4]
                user['email'] = row[5]
                user['admin'] = row[6]
                user['blocked'] = row[7]
                user['quota'] = row[8]
                user['galaxy'] = None

                if row[9] is not None and row[10] is not None:
                    user['galaxy'] = {
                        'url': row[9],
                        'apikey': row[10]
                    }

                users.append(user)

        return users

    def set_admin(self, new_status, username):
        """Set a new admin status to a user

        Parameters
        ----------
        new_status : boolean
            True for an admin
        username : string
            The concerned username
        """
        database = Database(self.app, self.session)

        query = '''
        UPDATE users
        SET admin=?
        WHERE username=?
        '''

        database.execute_sql_query(query, (new_status, username))

    def set_blocked(self, new_status, username):
        """Set a new blocked status to a user

        Parameters
        ----------
        new_status : boolean
            True for blocked
        username : string
            The concerned username
        """
        database = Database(self.app, self.session)

        query = '''
        UPDATE users
        SET blocked=?
        WHERE username=?
        '''

        database.execute_sql_query(query, (new_status, username))

    def set_quota(self, quota, username):
        """Set a new quota to a user

        Parameters
        ----------
        quota : int
            New quota
        username : string
            The concerned username
        """
        database = Database(self.app, self.session)

        query = '''
        UPDATE users
        SET quota=?
        WHERE username=?
        '''

        database.execute_sql_query(query, (Utils.humansize_to_bytes(quota), username))
