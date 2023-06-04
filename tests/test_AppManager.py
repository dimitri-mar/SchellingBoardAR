from unittest import TestCase
import os
import shutil

from DataApp.AppManager import AppManager
from DataApp.init_database import init_db

class TestAppManager(TestCase):

    def setUp(self) -> None:
        # let's use config.ini.AppManager for these tests
        if os.path.exists("config.ini"):
            os.rename("config.ini", "config.ini.backup")
        shutil.copy("config.ini.AppManager", "config.ini")
        if os.path.exists("data/test.db"):
            os.remove("data/test.db")
        init_db()


    def tearDown(self) -> None:
        # remove config.ini files
        os.remove("config.ini")
        if os.path.exists("config.ini.backup"):
            os.rename("config.ini.backup", "config.ini")

    # before starting
    def testAppManager(self) -> None:
        # create AppManager object
        app_manager = AppManager()
        print("app_manager created")
        assert app_manager is not None # check if object is not None

    def testAppManager_db_connection(self) -> None:
        # create AppManager object
        app_manager = AppManager()
        app_manager.init_db_connection()
        print("app_manager created")
        assert app_manager is not None # check if object is not None
