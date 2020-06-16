from genocrowd.libgenocrowd.Params import Params


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

    def update_position_info(self, id, attribute, new_value):
        updated_gene = self.genes.files.find_one_and_update({"_id": id}, {"$set": {attribute: new_value}})
        return updated_gene

    def get_all_positions(self):
        return list(self.genes.find({}))

    def store_answers_from_user(self, username, data):
        response = self.answers.find_one_and_update({"username": username})
        if response:
            self.answers.update_one({"username": username}, {"$set": {str(len(response) + 1): data}})
        else:
            self.answers[username].insert_one({"1": data})

    def define_questions(self, file):
        print("todo")
