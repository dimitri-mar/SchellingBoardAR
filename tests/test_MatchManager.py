import os
import shutil
from unittest import TestCase

from DataApp.init_database import init_db
from DataApp.AppManager import AppManager
from MatchManager.MatchManager import MatchManager


class TestMatchManager(TestCase):
    def setUp(self) -> None:
        # let's use config.ini.AppManager for these tests
        if os.path.exists("config.ini"):
            os.rename("config.ini", "config.ini.backup")
        shutil.copy("config.ini.AppManager", "config.ini")
        if os.path.exists("data/test.db"):
            os.remove("data/test.db")
        init_db()

        self.app_manager = AppManager()
        self.app_manager.init_db_connection()

    def tearDown(self) -> None:
        # remove config.ini files
        os.remove("config.ini")
        if os.path.exists("config.ini.backup"):
            os.rename("config.ini.backup", "config.ini")

    def test__init__(self):
        mm = MatchManager(self.app_manager.db_engine)


    def test_possible_dynamics(self):
        mm = MatchManager(self.app_manager.db_engine)
        assert mm.possible_dynamics is not None
        assert len(mm.possible_dynamics) > 0

        for d in mm.possible_dynamics:
            print(d)


    def test_get_available_name_description(self):
        mm = MatchManager(self.app_manager.db_engine)
        assert "free" in mm.get_available_name_description().keys()

    def test_create_match(self):
        mm = MatchManager(self.app_manager.db_engine)
        mm.create_match(["A","B","C"],
                        ["free",],
                        [42,])
        print("is match started? ", mm.is_match_started())
        print("get_open_match", mm.get_open_match())
        assert  mm.is_match_started()

    def test_get_board(self):
        mm = MatchManager(self.app_manager.db_engine)
        mm.create_match(["A", "B", "C"],
                        ["free", "free", "free"],
                        [42, 32, 45])

        print(mm.get_board("A"))
        assert mm.get_board("A").name == "A"


    def test_get_open_game(self):
        mm = MatchManager(self.app_manager.db_engine)
        mm.create_match(["A","B","C"],
                        ["free", "free", "free"],
                        [42, 32, 45])

        print(mm.match.games)
        b = mm.get_board("A")
        print("games", mm.get_open_game(b))

    def test_save_image_db(self):
        from  DataManagement.MatchDatabase import Picture
        mm = MatchManager(self.app_manager.db_engine)
        mm.create_match(["A", "B", "C"],
                        ["free", "free", "free"],
                        [42, 32, 45])

        pic = Picture()
        pic = Picture(picture_user_id="a",
                        picture_hash="pic_hash",
                        picture_path="pic_path",
                        )
        b = mm.get_board("A")
        og =  mm.get_open_game(b)
        #og.pictures.append(pic)

        pic = Picture(picture_user_id="a",
                        picture_hash="pic_hash",
                        picture_path="pic_path",
                        game_per_board=og)

        print("games", mm.get_open_game(b))


        #assert mm.get_open_game("A") is not None



    #
    # def test__init_db_session(self):
    #     self.fail()
    #
    # def test_get_open_match(self):
    #     self.fail()

