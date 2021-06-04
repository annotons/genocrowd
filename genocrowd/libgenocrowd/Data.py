from flask import current_app as ca

from genocrowd.libgenocrowd.LocalAuth import LocalAuth
from genocrowd.libgenocrowd.Params import Params

import gridfs


class Data(Params):
    """Manage DB"""
    def __init__(self, app, session):
        """init

        Parameters
        ----------
        app : Flask
            flask app
        session :
            Genocrowd session, contains the user
        """
        Params.__init__(self, app, session)
        self.genes = self.app.mongo.db["genes.files"]
        self.users = self.app.mongo.db["users"]
        self.answers = self.app.mongo.db["answers"]
        self.groups = self.app.mongo.db["groups"]

    def get_user_level(self, username):
        user = self.users.find_one({"username": username})
        return user["level"]

    def get_all_positions(self):
        return list(self.genes.find({}))

    def count_all_genes(self):
        return self.genes.count_documents({})

    def get_current_annotation(self, username):
        user = self.users.find_one({"username": username})
        return user["current_annotation"]

    def update_current_annotation(self, username, data):
        """Set a new currently annotated for a user

        Parameters
        ----------
        username : string
            The concerned username
        data : json
            Gene attributes
        """
        self.users.find_one_and_update({
            'username': username}, {
                '$set': {
                    'current_annotation': data
                }})

    def store_answers_from_user(self, username, data):
        db = ca.mongo.db
        fs = gridfs.GridFS(db, collection="answers")
        gene = self.get_current_annotation(username)
        fs.put(data.encode(), _id=gene["_id"], chromosome=gene["chromosome"], start=gene["start"], end=gene["end"], strand=gene["strand"], isAnnotable=True)
        gene = self.update_current_annotation(username, None)

    def get_number_of_answers(self):
        """get the number of annotations in the database

        Return
        ------
        int
            Number of annotation
        """
        return self.answers.count_documents({})

    def initiate_groups(self):
        self.groups.insert({
            'groupsAmount': 2
        })

    def get_number_of_groups(self):
        """get the number of groups

        Return
        ------
        int
            Number of groups
        """
        amount = self.groups.find_one({'groupsAmount': {'$exists': True}})
        return amount['groupsAmount']

    def set_number_of_groups(self, data):
        """Update the number of groups and create each group in the database

        Parameters
        ----------
        data : dict
            New number of groups

        Returns
        -------
        dict
            error, error message and updated number of groups
        """
        error = False
        error_message = []
        newNumber = int(data['newNumber'])
        groupsAmount = self.get_number_of_groups()

        if newNumber >= 2:
            updated_number = self.groups.update(
                {'groupsAmount': groupsAmount},
                {'$set': {
                    'groupsAmount': newNumber
                }})

        """Deleting documents containing old groups"""
        self.groups.remove({"number": {'$exists': True}})

        """Creation of new empty groups"""
        for i in range(newNumber):
            self.groups.insert({'number': i + 1, 'name': "", 'student': []})

        return {
            'error': error,
            'errorMessage': error_message,
            'groupsAmount': updated_number
        }

    def get_all_groups(self):
        """Get all groups info

        Returns
        -------
        list
            All groups info
        """
        groupCursor = self.groups.find({"number": {'$exists': True}})
        groupList = []
        for document in groupCursor:
            document['_id'] = str(document['_id'])
            groupList.append(document)
        return groupList

    def update_group_name(self, data):
        error = False
        error_message = []
        name = data['name']
        number = int(data['number'])

        self.groups.find_one_and_update({
            'number': number},
            {'$set': {
                'name': name
            }})

        return{
            'error': error,
            'error_message': error_message,
            'name': name
        }

    def get_top_annotation(self):
        """Get top annotator and top group

        Returns
        -------
            dict
                list of top 3 users and groups, error and error message

        """
        error = False
        error_message = []
        top_users = []
        top_groups = []
        nb = self.get_number_of_groups()
        liste_temp = [0] * nb
        userList = LocalAuth.get_all_users(self)

        for element in userList:
            """We don't want Admin in the ranking"""
            if element['group'] is not None:
                dico = {}
                dico["username"] = element['username']
                dico["score"] = element['total_annotation']
                top_users.append(dico)

                """sums the annotations for each group"""
                index = element['group'] - 1
                liste_temp[index] = liste_temp[index] + element['total_annotation']

        """get the group name"""
        groups_names = self.get_groups_names()
        for i, element in enumerate(liste_temp):
            dico = {}

            dico["name"] = groups_names['groups_names'][i]
            dico["score"] = element
            top_groups.append(dico)

        top_groups = sorted(top_groups, key=lambda k: k['score'], reverse=True)
        top_users = sorted(top_users, key=lambda k: k['score'], reverse=True)

        return {
            'top_users': top_users[:3],
            'top_groups': top_groups[:3],
            'error': error,
            'errorMessage': error_message
        }

    def get_groups_names(self):
        """Get groups name

        Returns
        -------
            dict
                error, error message and list of groups names
        """
        error = False
        error_message = []
        groups_names = []
        groupCursor = self.groups.find({'number': {'$exists': True}})
        for document in groupCursor:
            document['_id'] = str(document['_id'])
            groups_names.append(document['name'])
        return {
            'groups_names': groups_names,
            'error': error,
            'errorMessage': error_message
        }

    def find_genes_level(self, maliste, value):
        """Select genes according to a difficulty level

        Returns
        -------
        list
            dict
                chromosome, start, end, strand, isAnnotable, difficulty, priority, tags
        """
        good_difficulty = []
        for element in maliste:
            if element['difficulty'] == value:
                good_difficulty.append(element)
        return good_difficulty

    def select_genes(self, i, maliste):
        """Select the list of genes whose difficulty matches the user's level

        Returns
        -------
            list
                dict
                    chromosome, start, end, strand, isAnnotable, difficulty, priority, tags
        """
        switcher = {
            0: self.find_genes_level(maliste, 1521)
            # TODO complete switcher
        }
        return switcher.get(i, "Invalid level number")
