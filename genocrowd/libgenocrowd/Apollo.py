from genocrowd.libgenocrowd.Params import Params


class Apollo(Params):
    """Manage Apollo interactions"""
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
        self.position = self.app.mongo.db["position"]
        self.questions = self.app.mongo.db["questions"]
        self.users = self.app.mongo.db["users"]
        self.answers = self.app.mongo.db["answers"]

    def get_all_questions(self):
        return list(self.questions.find({}))

    def get_gene_associated_questions(self, position):
        return list(self.questions.find({"position": position}))

    def add_position_to_db(self, positiondata):
        self.position.insert({
            "chromosome": positiondata["chromosome"],
            "strand": positiondata["chromosome"],
            "position": positiondata["position"],
            "specificQuestions": positiondata["specificQuestions"]
        })

    def add_batch_position_to_db(self, batchdata):

        for pos in batchdata:
            self.add_position_to_db(pos)

    def add_question_on_the_fly(self, data):
        gene = data['position']
        text = data['text']
        self.questions.insert({
            'position': gene,
            'text': text
        })

    def get_all_positions(self):
        return list(self.position.find({}))

    def store_answers_from_user(self, username, data):
        response = self.answers.find_one_and_update({"username": username, })
        if response:
            self.answers.update_one({"username": username}, {"$set": {str(len(response) + 1): data}})
        else:
            self.answers[username].insert_one({"1": data})
