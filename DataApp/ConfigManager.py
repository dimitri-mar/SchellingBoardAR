import configparser
from dotenv import load_dotenv, find_dotenv
from loguru import logger
import os
from typing import Dict


def parse_env_variables() -> Dict:
    """ parse environent variables"""
    load_dotenv(find_dotenv(usecwd=True))

    prefix = "SCHELLING_"

    # remove prefix and convert to lower case
    env_conf = {
        k.lower()[len(prefix):]: v for k, v in os.environ.items()
            if k.startswith(prefix)
    }
    return env_conf


def parse_config_file() -> Dict:
    """Load configuration from config.ini
    """

    config = configparser.ConfigParser()
    config.read("config.ini")

    return config


class DbConfig:
    def __init__(self, config, config_from_env):
        self.db_type = None
        self.db_path = None

        self.connection = None
        self._config = config["Database"]
        self._config_from_env = config_from_env

        self.set_values_from_configs()

    def get_from_configs(self, name:str):
        """return values from config prioritizing env variables"""
        if "db_" + name in self._config_from_env.keys():
            return self._config_from_env[ "db_" + name]
        elif name in self._config.keys():
            return self._config[name]
        else:
            return None

    def set_values_from_configs(self ):
        self.db_type = self.get_from_configs("type")
        self.path = self.get_from_configs("path")
        if self.db_type != "sqlite":
            self.path = None
            self.connection = {}
            self.connection["host"] = self.get_from_configs("host")
            self.connection["port"] = self.get_from_configs("port")
            self.connection["user"] = self.get_from_configs("user")
            self.connection["password"] = self.get_from_configs("password")
            self.connection["database"] = self.get_from_configs("database")

    def check_db_parameters(self, error=False):
        if self.db_path == "sqlite":
            if error:
                assert self.db_path is not None, "db_path is missing"
            return self.db_path is not None
        elif self.db_path == "postgres":
            if error:
                assert self.connection is not None, "db_path is missing"
            return self.connection is not None


class Config:

    def __init__(self):

        # I set the default config values
        self.run_management_application = True
        self.sys_log_save = True
        self.sys_log_level = "DEBUG"
        self.use_database = True
        self.output_dir = "data"
        self.db = None

        self._config = configparser.ConfigParser()
        self._config.read("config.ini")
        self._config_from_env = parse_env_variables()

        # I set the values from the file and from the environment variables
        self.set_values_from_configs()

    def print_config_raw(self):
        for section in self._config.sections():
            print(f"Section: {section}")
            for key in self._config[section]:
                print(f"    {key} = {self._config[section][key]}")

    def set_values_from_configs(self) -> None:
        logger.debug("Setting values from config.ini and environment variables")
        self.use_database =\
            not self._config["General"].getboolean("without_database")
        logger.debug(f"Database is enabled: {self.use_database}")

        self.sys_log_save = \
            self._config["General"].getboolean("sys_log_save")
        self.log_level = \
            self._config["General"]["log_level"]
        self.output_dir = \
            self._config["General"]["output_dir"]


        if self.use_database:
            logger.debug("Database is enabled, importing db config")
            self.db = DbConfig(self._config, self._config_from_env)
            self.db.check_db_parameters(error=True)




if __name__ == "__main__":
    pass
