import time

from apollo import ApolloInstance

from flask import current_app as ca


class ApolloUsers(object):
    """Allows the management of the Apollo users"""

    def __init__(self):
        self.wa = ApolloInstance(ca.apollo_url, ca.apollo_admin_email, ca.apollo_admin_password)

    def add_user(self, username, email, password, role="user"):
        """ Add a user to Apollo and creates a copy of the studied genome for him

        Returns
        -------

        json
            user: dict
        """
        users = self.wa.users.get_users()
        user = {}
        for u in users:
            if u['username'] == email:
                user = u

        if len(user) == 1:
            # Update name, regen password if the user ran it again
            returnData = self.wa.users.update_user(
                email, username, username, password)
        else:
            returnData = self.wa.users.create_user(
                email, username, username, password, role=role)

        org_id = "{}_{}".format(ca.apollo_org_id, email)

        orgs = self.wa.organisms.get_organisms()
        ca.logger.info("Got this org list from apollo: %s" % orgs)
        no_orgs = 'error' in orgs and orgs['error'] == 'Not authorized for any organisms'
        if not no_orgs:
            orgs_ids = [org['id'] for org in orgs]
        if no_orgs or org_id not in orgs_ids:
            self.wa.organisms.add_organism(
                org_id,
                ca.apollo_dataset_path,
                genus='Acyrthosiphon',
                species='pisum',
                public=False)
            time.sleep(2)
            self.wa.users.update_organism_permissions(
                email,
                org_id,
                write=True,
                export=True,
                read=True,
            )
        return returnData
