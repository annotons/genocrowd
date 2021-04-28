"""Contain the Database Auth Dialog Class"""

import random
from datetime import datetime

from flask_pymongo import BSONObjectIdConverter

from genocrowd.libapollo.ApolloUsers import ApolloUsers
from genocrowd.libgenocrowd.Params import Params

from pymongo import ReturnDocument

from validate_email import validate_email

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
        self.users = self.app.mongo.db["users"]
        self.groups = self.app.mongo.db["groups"]

    def check_inputs(self, inputs):
        """Check user inputs

        Check if inputs are not empty, if passwords are identical, and if
        username and email are not already in the database

        Parameters
        ----------
        inputs : dict
            User inputs

        """

        if not inputs['username'] or inputs['username'] == '':
            self.error = True
            self.error_message.append('Username name empty')

        if not validate_email(inputs['email']):
            self.error = True
            self.error_message.append('Not a valid email')

        if not inputs['password']:
            self.error = True
            self.error_message.append('Password is empty')

        if inputs['password'] != inputs['passwordconf']:
            self.error = True
            self.error_message.append("Password doesn't match")

        if self.is_username_in_db(inputs['username']):
            self.error = True
            self.error_message.append('Username already registered')

        if self.is_email_in_db(inputs['email']):
            self.error = True
            self.error_message.append('Email already registered')

    def get_error(self):

        return self.error

    def get_error_message(self):

        return self.error_message

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
        response = self.users.find_one({'username': username})
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
        response = self.users.find_one({'email': email})
        if response:
            return True
        else:
            return False

    def get_number_of_users(self):
        """get the number of self.users in the DB

        Returns
        -------
        int
            Number of user in the Database
        """
        return self.users.count_documents({})

    def add_user_to_database(self, username, email, password, grade, role="user"):

        self.app.logger.info("Creating user %s" % username)
        password = self.app.bcrypt.generate_password_hash(password).decode('utf-8')
        created = datetime.utcnow()
        grade = grade.upper()
        user_id = self.users.insert({
            'username': username,
            'email': email,
            'password': password,
            'created': created,
            'isAdmin': role == 'admin',
            'isExternal': False,
            'blocked': False,
            'current_annotation': None,
            'grade': grade,
            'groupe': None
        })

        new_user = self.users.find_one({'_id': user_id})

        apolloinstance = ApolloUsers()
        apolloinstance.add_user(username, email, password, role)

        return new_user

    def authenticate_user(self, data):
        """
        check if the password is the good password
            associated with the email or the username

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
        user = {}
        error_message = []
        if self.is_username_in_db(login):
            response = self.users.find_one({'username': login})

            if self.app.bcrypt.check_password_hash(response['password'], password):
                error = False
                response['_id'] = str(response['_id'])
                user = response
            else:
                error = True
                error_message.append("Invalid password")

        elif self.is_email_in_db(login):
            response = self.users.find_one({'email': login})
            if self.app.bcrypt.check_password_hash(response['password'], password):
                error = False
                response['_id'] = str(response['_id'])

                user = response
            else:
                error = True
                error_message.append("Invalid password")
        else:
            error = True
            error_message.append("Incorrect login identifier")

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
        error = False
        error_message = []
        username = data['newUsername']
        email = data['newEmail']
        if len(username) == 0:
            assert username != user['username']
            username = user['username']
        if len(email) == 0:
            email = user['email']
        bson = BSONObjectIdConverter(BaseConverter)
        updated_user = self.users.find_one_and_update({
            '_id': bson.to_python(user['_id'])}, {
                '$set': {
                    'username': username,
                    'email': email
                }}, return_document=ReturnDocument.AFTER)
        assert updated_user['username'] == username
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
        updated_user = user

        # check if new passwords are identicals
        password_identical = (inputs['newPassword'] == inputs['confPassword'])

        if not inputs["newPassword"] == '':
            if password_identical:
                # Try to authenticate the user with his old password
                credentials = {
                    'login': user['username'],
                    'password': inputs['oldPassword']}
                authentication = self.authenticate_user(credentials)
                if not authentication['error']:
                    # Update the password
                    password = self.app.bcrypt.generate_password_hash(
                        inputs['newPassword']).decode('utf-8')
                    bson = BSONObjectIdConverter(BaseConverter)
                    updated_user = self.users.find_one_and_update({
                        '_id': bson.to_python(user['_id'])}, {
                            '$set': {
                                'password': password
                            }}, return_document=ReturnDocument.AFTER)
                else:
                    error = True
                    error_message = 'Incorrect old password'
            else:
                error = True
                error_message = 'New passwords are not identical'
        else:
            error = True
            error_message = 'Empty password'
        return {
            'error': error,
            'error_message': error_message,
            'user': updated_user}

    def get_all_users(self):
        """Get all user info

        Returns
        -------
        list
            All user info
        """
        userCursor = list(self.users.find({}))
        userList = []
        for document in userCursor:
            document['_id'] = str(document['_id'])
            userList.append(document)
        return userList

    def set_admin(self, new_status, username):
        """Set a new admin status to a user

        Parameters
        ----------
        new_status : boolean
            True for an admin
        username : string
            The concerned username
        """
        self.users.find_one_and_update({
            'username': username}, {
                '$set': {
                    'isAdmin': new_status
                }})

    def set_blocked(self, new_status, username):
        """Set a new blocked status to a user

        Parameters
        ----------
        new_status : boolean
            True for blocked
        username : string
            The concerned username
        """
        self.users.find_one_and_update({
            'username': username}, {
                '$set': {
                    'blocked': new_status
                }})

    def set_group(self, data):
        """Assign a group to each student

        Parameters
        ----------
        groupsamount : str
            Number of groups

        Return
        ------
        dict
            error, error message and the list of grades
        """
        error = False
        error_message = []
        gradeList = self.users.distinct("grade")
        gradeList.remove('ADMIN')
        max_group = int(data["groupsAmount"])
        groupNumber = 1
        bson = BSONObjectIdConverter(BaseConverter)

        for element in gradeList:
            userCursor = list(self.users.find({'grade': element}))
            userList = []

            for document in userCursor:
                document['_id'] = str(document['_id'])
                userList.append(document)

            random.shuffle(userList)
            for user in userList:
                if groupNumber > max_group:
                    groupNumber = 1
                    self.users.find_one_and_update({
                        '_id': bson.to_python(user['_id'])}, {
                            '$set': {'group': groupNumber}}, return_document=ReturnDocument.AFTER)
                    self.groups.update({
                        'number': groupNumber}, {
                            '$push': {'student': user}})
                else:
                    self.users.find_one_and_update({
                        '_id': bson.to_python(user['_id'])}, {
                            '$set': {'group': groupNumber}}, return_document=ReturnDocument.AFTER)
                    self.groups.update({
                        'number': groupNumber}, {
                            '$push': {'student': user}})
                groupNumber += 1

        return {
            'error': error,
            'errorMessage': error_message,
            'gradeList': gradeList
        }
