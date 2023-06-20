from unittest import TestCase
import os
import shutil

from DataApp.ConfigManager import parse_env_variables, Config


class TestConfigManager(TestCase):
    # to begin we rename .env.configtest to .env
    def setUp(self) -> None:
        # lets use config.ini.configtest and .env.configtest
        if os.path.exists(".env"):
            os.rename(".env", ".env.backup")
        shutil.copy(".env.configtest", ".env")
        if os.path.exists("config.ini"):
            os.rename("config.ini", "config.ini.backup")
        shutil.copy("config.ini.configtest", "config.ini")

    def tearDown(self) -> None:
        # remove .env and config.ini files
        os.remove(".env")
        if os.path.exists(".env.backup"):
            os.rename(".env.backup", ".env")
        os.remove("config.ini")
        if os.path.exists("config.ini.backup"):
            os.rename("config.ini.backup", "config.ini")

    def test_parse_env_variables(self):
        print(os.getcwd())
        conf_env = parse_env_variables()
        print(conf_env)
        self.assertEqual(conf_env['istest'], '1')

    def test_Config(self):
        print("Testing config")
        print(os.getcwd())
        config = Config()
        config.print_config_raw()
        print(config._config_from_env)

        self.assertEqual(config.db.db_type, 'postgres')
        self.assertIsNone(config.db.path)
        self.assertEqual(config.db.connection["port"], "2")



