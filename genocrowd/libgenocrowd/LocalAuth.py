"""Contain the Database class"""

from genocrowd.libgenocrowd.Params import Params

from validate_email import validate_email


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
        if not inputs['fname']:
            self.error = True
            self.error_message.append('First name empty')

        if not inputs['lname']:
            self.error = True
            self.error_message.append('Last name empty')

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

    def authenticate_user_with_apikey(self, apikey):
        """
        Return the user associated with the API key

        Parameters
        ----------
        inputs : string
            API key

        Returns
        -------
        dict
            user info if authentication success
        """

    def authenticate_user(self, inputs):
        """
        check if the password is the good password associate with the email

        Parameters
        ----------
        inputs : dict
            login and password

        Returns
        -------
        dict
            user info if authentication success
        """

    def update_profile(self, inputs, user):
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

    def update_apikey(self, user):
        """Create a new api key and store in the database

        Parameters
        ----------
        user : dict
            The current user

        Returns
        -------
        dict
            error, error message and updated user
        """

    def get_user(self, username):
        """Get a specific user by his username

        Parameters
        ----------
        username : string
            User username

        Returns
        -------
        dict
            The corresponding user
        """

    def get_all_users(self):
        """Get all user info

        Returns
        -------
        list
            All user info
        """

    def set_admin(self, new_status, username):
        """Set a new admin status to a user

        Parameters
        ----------
        new_status : boolean
            True for an admin
        username : string
            The concerned username
        """

    def set_blocked(self, new_status, username):
        """Set a new blocked status to a user

        Parameters
        ----------
        new_status : boolean
            True for blocked
        username : string
            The concerned username
        """

    def set_quota(self, quota, username):
        """Set a new quota to a user

        Parameters
        ----------
        quota : int
            New quota
        username : string
            The concerned username
        """
