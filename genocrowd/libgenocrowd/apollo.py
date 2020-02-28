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
        self.genes = self.app.mongo.db["genes"]
        self.questions = self.app.mongo.db["questions"]

    def get_all_questions(self):
        return list(self.questions.find({}))

    def get_gene_associated_questions(self, gene):
        return list(self.questions.find({"gene": gene}))

    def add_question_on_the_fly(self, data):
        gene = data['gene']
        text = data['text']
        self.questions.insert({
            'gene': username,
            'Text': email
        })

    def get_all_genes(self):
        return list(self.genes.find({}))
