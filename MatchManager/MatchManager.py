from sqlalchemy.orm import sessionmaker

from DataManagement.MatchDatabase import Match, Game, Board, Base




class MatchManager:
    """ The MatchManager is the class that manages the creation of matches and
    games.

    It is the only class that has access to the database, and it is the only
    class that can create new matches and games.

    only one Match at the time is handled. Therefore at init time the MatchManager
    will look for a match in the database that has not been closed yet.
    """

    def __init__(self, db_engine):
        """ create a new MatchManager

        Args:
            db_engine: a sqlalchemy engine object that points to the database
        """
        self.db_engine = db_engine
        self.db_session = None
        self._init_db_session()

        # check if there is a match that is not closed yet
        self.match = self.get_open_match()
        if self.match is None:
            self.match = self.create_match()

    def _init_db_session(self):
        """ create a new database session """
        Session = sessionmaker(bind=self.db_engine)
        self.db_session = Session()

    def get_open_match(self):
        """ return the match that is not closed yet

        Returns:
            Match object or None
        """
        return self.db_session.query(Match).filter(Match.ending_time == None).first()
