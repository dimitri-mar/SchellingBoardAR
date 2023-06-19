""" The MatchManager is the class that manages the creation and the developement
of matches and games.
"""
from typing import List
from loguru import logger
import datetime

from sqlalchemy.orm import sessionmaker

from DataManagement.MatchDatabase import Match, Game, Board, SGdynamics
from DataManagement.MatchDatabase import GamePerBoard, Picture


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
        logger.debug(f"open match {self.match}")


    def _init_db_session(self):
        """ create a new database session """
        Session = sessionmaker(bind=self.db_engine)
        self.db_session = Session()

    def get_open_match(self):
        """ return the match that is not closed yet

        Returns:
            Match object or None
        """
        matches =  self.db_session.query(Match). \
            filter(Match.ending_time.is_(None) ). \
            all()

        if len(matches) == 0:
            return None
        elif len(matches) == 1:
            return matches[0]
        else:
            raise Exception("more than one match is open")

    def is_match_started(self) -> bool:
        """ return True if there is an open match

        Returns:
            bool
        """

        if self.match is None:
            self.match = self.get_open_match()

        return self.match is not None

    @property
    def possible_dynamics(self):
        if self._possible_dynamics is None:
            self._possible_dynamics = self.db_session.query(SGdynamics).all()
            return self._possible_dynamics
        else:
            return self._possible_dynamics

    def get_available_name_description(self):
        return {d.name: d.description for d in self.possible_dynamics}

    def get_available_dynamics_labels(self):
        return {d.id: d.name for d in self.possible_dynamics}

    def get_available_dynamics_dict(self):
        return {d.name: d for d in self.possible_dynamics}

    def create_match(self, boards: List[str],
                     game_types: List[str],
                     game_times: List[int]):

        logger.debug("creating a new match")
        logger.debug(f"the match is compose of {len(game_types)} games")
        logger.debug(f"Each game will be played for a maximum of"
                     f" {game_times} games")

        match = Match()

        # let's start from the boards
        boards_db = []
        for board in boards:
            logger.debug(f"board: {board}")
            boards_db.append(Board(name=board))

        match.boards = boards_db

        dy_types_dict = self.get_available_dynamics_dict()
        games_db = []
        for ix, (g_type, g_time) in enumerate(zip(game_types, game_times)):
            logger.debug(f"game type: {g_type}, game time: {g_time}")

            games_db.append(Game(game_dynamics=dy_types_dict[g_type],
                                 max_time_minutes=g_time,
                                 order_in_match=ix + 1
                                 ))
        match.games = games_db

        # every board is going to play every game
        for board in boards_db:
            for game in games_db:
                if game.order_in_match == 1:
                    starting_time = datetime.datetime.now()
                else:
                    starting_time = None
                board.games_per_board.append(
                    GamePerBoard(
                        board=board,
                        game=game,
                        starting_time=starting_time
                    )
                )

        print("creating a new match")
        self.db_session.add(match)
        self.db_session.commit()
        self.match = match

    def get_boards(self):
        return self.match.boards

    def end_match(self):
        """ end the match """
        self.match.ending_time = datetime.datetime.now()
        self.db_session.add(self.match)
        self.db_session.commit()

    def get_board(self, name:str):
        """ return the board with the given name

        Args:
            name: str

        Returns:
            Board object
        """
        boards_names = [b.name for b in self.match.boards]
        ix_board = boards_names.index(name)
        return self.match.boards[ix_board]




    def get_open_game(self, board):
        for game_per_board in board.games_per_board:
            if game_per_board.ending_time is None:
                return game_per_board

    def save_image_db(self,
                      user_id,
                      pic_hash,
                      pic_path,
                      board_name):
        """ save the image in the database """
        board = self.get_board(board_name)
        game = self.get_open_game(board)


        pic = Picture(picture_user_id=user_id,
                        picture_hash=pic_hash,
                        picture_path=pic_path,
                        )
        game.pictures.append(pic)
        #self.db_session.add(pic)
        self.db_session.commit()





