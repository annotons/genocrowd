import time

from apollo import ApolloInstance


class ApolloUsers(object):

    def __init__(self):
        self.wa = ApolloInstance(
            'http://localhost:8080/apollo', 'admin@admin.fr', "admin")

    def add_user(self, data):
        print(data)
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
                data['email'], data['username'], data['username'], data['password'], role='user')
            self.wa.organisms.add_organism(
                "puceron_{}".format(data["email"]),
                "/home/konogan/Téléchargements/apisum_v3",
                genus='Saccharomyces',
                species='cerevisiae',
                public=False)
            time.sleep(2)
            self.wa.users.update_organism_permissions(
                data["email"],
                "puceron_{}".format(data["email"]),
                write=True,
                export=True,
                read=True,
            )
            # modif = self.wa.annotations.add_feature(feature={}, organism=, sequence=None)
        return returnData

    def log_user(self, data):
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
