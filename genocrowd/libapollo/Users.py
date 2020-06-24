import time

from apollo import ApolloInstance

from flask import current_app as ca


class ApolloUsers(object):
    """Allows the management of the Apollo users """

    def __init__(self):
        self.wa = ApolloInstance(
            'http://localhost:8888', ca.apollo_admin_email, ca.apollo_admin_password)

    def add_user(self, data):
        """ Add a user to Apollo and creates a copy of the studied genome for him

    Returns
    -------

    json
        user: dict
    """
        users = self.wa.users.get_users()
        user = {}
        for u in users:
            if u['username'] == data['email']:
                user = u

        if len(user) == 1:
            # Update name, regen password if the user ran it again
            returnData = self.wa.users.update_user(
                data['email'], data['username'], data['username'], data['password'])
        else:
            returnData = self.wa.users.create_user(
                data['email'], data['username'], data['username'], data['password'], role=data['role'])
            self.wa.organisms.add_organism(
                "puceron_{}".format(data["email"]),
                "/data/dataset",
                genus='Acyrthosiphon',
                species='pisum',
                public=False)
            time.sleep(2)
            self.wa.users.update_organism_permissions(
                data["email"],
                "puceron_{}".format(data["email"]),
                write=True,
                export=True,
                read=True,
            )
        return returnData

    def log_user(self, data):
        """ Add a user to Apollo and creates a copy of the studied genome for him

    Returns
    -------

    json
        user: dict
    """
        users = self.wa.users.get_users()
        user = [u for u in users
                if u['username'] == data['email']]

        if len(user) == 1:
            # Update name, regen password if the user ran it again
            returnData = self.wa.users.update_user(
                data['email'], data['username'], data['username'], data['password'])
        else:
            returnData = self.wa.users.create_user(
                data['email'], data['username'], data['username'], data['password'], role='user')
        return returnData
