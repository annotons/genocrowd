from time import time

from apollo import ApolloInstance


class ApolloUsers(object):
    # def _init_(self):
    def add_user(self, data):

        wa = ApolloInstance('http://localhost:8080/annotator/index', 'admin@admin.fr', "admin")

        time.sleep(1)
        users = wa.users.get_users()
        user = [u for u in users
                if u['username'] == data['email']]

        if len(user) == 1:
            # Update name, regen password if the user ran it again
            returnData = wa.users.update_user(data['email'], data['username'], data['username'], data['password'])
        else:
            returnData = wa.users.create_user(data['email'], data['username'], data['username'], data['password'], role='user')
        return returnData
