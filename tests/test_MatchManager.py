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


    #
    # def test__init_db_session(self):
    #     self.fail()
    #
    # def test_get_open_match(self):
    #     self.fail()

