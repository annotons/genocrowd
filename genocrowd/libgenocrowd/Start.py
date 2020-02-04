"""Contain the Start classe
"""

from genocrowd.libgenocrowd.Params import Params


class Start(Params):

    """Initialize the data directory and the database

    Attributes
    ----------
    database_path : str
        Path to the database file
    """

    def __init__(self, app, session):
        """Get database paths from the genocrowd settings

        Parameters
        ----------
        app :
            flask app
        session :
            flask session
        """
        Params.__init__(self, app, session)

        self.database_path = self.settings.get('genocrowd', 'database_path')

    def start(self):
        """Initialize the database file
        """
        self.create_database()

    def create_database(self):
        """Initialize the database file
        """
