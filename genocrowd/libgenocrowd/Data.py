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
