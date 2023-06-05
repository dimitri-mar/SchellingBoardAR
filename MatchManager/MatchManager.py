""" The MatchManager is the class that manages the creation and the developement
of matches and games.
"""
from sqlalchemy.orm import sessionmaker

from DataManagement.MatchDatabase import Match, Game, Board, Base, SGdynamics


class MatchManager:
    """ The MatchManager is the class that manages the creation of matches and
    games.

    It is the only class that has access to the database, and it is the only
    class that can create new matches and games.

    only one Match at the time is handled. Therefore, at init time the MatchManager
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

        self._possible_dynamics = None

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
        return self.db_session.query(Match).\
            filter(Match.ending_time is None).\
            first()

    def is_match_started(self) -> bool:
        """ return True if there is an open match

        Returns:
            bool
        """
        return self.match is not None

    @property
    def possible_dynamics(self):
        if self._possible_dynamics is None:
            self._possible_dynamics =  self.db_session.query(SGdynamics).all()
            return self._possible_dynamics
        else:
            return self._possible_dynamics

    def get_available_name_description(self):
        return {d.name: d.description for d in self.possible_dynamics}

    def get_available_dynamics_labels(self):
        return {d.id: d.name for d in self.possible_dynamics}



    def create_match(self):
        pass
