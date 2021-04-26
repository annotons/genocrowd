from flask import current_app as ca

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

    def get_all_positions(self):
        return list(self.genes.find({}))

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

    def set_number_of_groups(self, number):
        """Update the number of groups and create each group in the database

        Parameters
        ----------
        number : str
            New number of groups

        Returns
        -------
        dict
            error, error message and updated number of groups
        """
        error = False
        error_message = []
        newNumber = int(number)
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
            self.groups.insert({'number': i + 1, 'name': "", 'students': []})

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
