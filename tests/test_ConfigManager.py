from unittest import TestCase
import os

from DataApp.ConfigManager import parse_env_variables, Config


class Test(TestCase):
    # to begin we rename .env.configtest to .env
    def setUp(self) -> None:
        # rename .env to .env.backup
        if os.path.exists(".env"):
            os.rename(".env", ".env.backup")
        os.rename(".env.configtest", ".env")
    def tearDown(self) -> None:
        os.rename(".env", ".env.configtest")
        if os.path.exists(".env.backup"):
            os.rename(".env.backup", ".env")


    def test_parse_env_variables(self):
        print(os.getcwd())
        conf_env = parse_env_variables()
        print(conf_env)
        self.assertEqual(conf_env['istest'], '1')

    def test_Config(self):
        config = Config()
        self.assertEqual(config.db.db_type, 'postgres')
        self.assertIsNone(config.db.path)
        self.assertEqual(config.db.connection["port"], "2")



