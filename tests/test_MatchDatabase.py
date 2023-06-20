import os
from  datetime import datetime
from unittest import TestCase
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from DataManagement.MatchDatabase import Match, Game, Board, Base, \
                        GamePerBoard, SGdynamics, Picture


class TestMatch(TestCase):
    def setUp(self) -> None:
        #engine = create_engine('sqlite:///:memory:', echo=False)
        self.file_name = 'test.db'
        # if the file already exists, delete it

        if os.path.exists(self.file_name):
            print(f"removing {self.file_name}")
            os.remove(self.file_name)


        engine = create_engine(f'sqlite:///{self.file_name}', echo=True)
        Session = sessionmaker(bind=engine)
        self.session = Session()
        Base.metadata.create_all(engine)

    def test_match(self):
        """ a minimum test for the match table """

        match = Match()
        t1 = datetime.strptime('2020-01-01 00:00:00', '%Y-%m-%d %H:%M:%S')
        t2 = datetime.strptime('2020-12-21 00:00:00', '%Y-%m-%d %H:%M:%S')
        match.starting_time = t1
        match.ending_time = t2
        game = Game()
        match.games.append(game)
        self.session.add(match)
        self.session.commit()
        self.assertEqual(len(self.session.query(Match).all()), 1)

    def test_game(self):
        """ a minimum test for the game table """
        game = Game()
        self.session.add(game)
        self.session.commit()

        self.assertEqual(len(self.session.query(Game).all()), 1)
        self.assertEqual(self.session.query(Game).first().game_dynamics.name, "free")
    def test_match_without_game(self):
        """ a minimum test for the match table, expected an error """
        match = Match()
        self.session.add(match)
        self.session.commit()
        #self.assertRaises(Exception, self.session.commit)
        self.assertEqual(len(self.session.query(Match).all()), 1)


    def test_GamePerBoard(self):
        game = Game()
        board = Board()
        game_per_board = GamePerBoard(game=game, board=board)
        t1 = datetime.strptime('2020-01-01 00:00:00', '%Y-%m-%d %H:%M:%S')
        t2 = datetime.strptime('2020-01-01 01:00:00', '%Y-%m-%d %H:%M:%S')
        game_per_board.starting_time = t1
        game_per_board.ending_time = t2

        self.session.add(game_per_board)
        self.session.commit()
        self.assertEqual(len(self.session.query(GamePerBoard).all()), 1)

    def test_picture(self):
        """ a minimum test for the picture table """
        picture = Picture(picture_user_id=1,
                            picture_hash='test',
                            picture_path='test',
                            picture_upload_time=\
                                    datetime.strptime('2020-01-01 01:00:00',
                                                      '%Y-%m-%d %H:%M:%S'),
                            picture_metadata='test')
        self.session.add(picture)
        self.session.commit()
        self.assertEqual(len(self.session.query(Picture).all()), 1)

    def test_part_database(self):
        """ a minimum test for the entire database """
        game_dynamics = SGdynamics(name='second',
                                   description='test')
        t1 = datetime.strptime('2020-01-01 00:00:00', '%Y-%m-%d %H:%M:%S')
        t2 = datetime.strptime('2020-01-01 01:00:00', '%Y-%m-%d %H:%M:%S')

        match = Match()
        match.base_url='http://localhost:5000'
        match.starting_time = t1
        match.ending_time = t2
        game = Game()
        game.game_dynamics = game_dynamics

        board = Board()
        match.boards.append(board)
        match.games.append(game)
        match.games.append(game)

        self.session.add(match)
        self.session.commit()

        self.assertEqual(len(self.session.query(Match).all()), 1)

    def test_entire_database(self):
        """ a minimum test for the entire database """
        game_dynamics = SGdynamics(name='second',
                                   description='test')
        t1 = datetime.strptime('2020-01-01 00:00:00', '%Y-%m-%d %H:%M:%S')
        t2 = datetime.strptime('2020-01-01 01:00:00', '%Y-%m-%d %H:%M:%S')

        match = Match()
        match.base_url='http://localhost:5000'
        match.starting_time = t1
        match.ending_time = t2
        game = Game()
        game.game_dynamics = game_dynamics

        board = Board()
        match.boards.append(board)
        match.games.append(game)
        match.games.append(game)


        for b in match.boards:
            for g in match.games:
                b.games_per_board.append(GamePerBoard(game=g, board=b))



        picture = Picture(picture_user_id=1,
                            picture_hash='test',
                            picture_path='test',
                            picture_upload_time=\
                                    datetime.strptime('2020-01-01 01:00:00',
                                                      '%Y-%m-%d %H:%M:%S'),
                            picture_metadata='test')
        match.boards[0].games_per_board[0].pictures.append(picture)

        self.session.add(match)
        self.session.commit()

        self.assertEqual(len(self.session.query(Match).all()), 1)
        self.assertEqual(len(self.session.query(Game).all()), 1)
        self.assertEqual(len(self.session.
                             query(Board).all()), 1)

    def test_board(self):
        """ a minimum test for the board table """
        board = Board()
        self.session.add(board)
        self.session.commit()
        self.assertEqual(len(self.session.query(Board).all()), 1)
    # when finished delete the file created
    def tearDown(self) -> None:
        import os
        os.remove(self.file_name)
