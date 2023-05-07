import os
from unittest import TestCase
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from DataManagement.MatchDatabase import Match, Game, Board, Base



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
        game = Game()
        match.games.append(game)
        self.session.add(match)
        self.session.commit()
        self.assertEqual(len(self.session.query(Match).all()), 1)

    # when finished delete the file created
    def tearDown(self) -> None:
        import os
        os.remove(self.file_name)
