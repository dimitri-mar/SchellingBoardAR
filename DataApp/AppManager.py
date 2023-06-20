""" AppManager.py handles all the configuration and initialization of the application
    It is the first script to be run when the application starts
    It provides the connection to the database.
"""

from sqlalchemy import create_engine
from sqlalchemy_utils.functions import database_exists

from DataApp.ConfigManager import Config
from loguru import logger
import sys


class AppManager:
    def __init__(self):
        self.sys_log_save_handler = None
        logger.info("Initializing AppManager")
        self.config = Config()
        logger.debug("Config loaded")
        self.logger_init()
        logger.debug("Logger initialized")

        if self.config.use_database:
            self.db_engine = None

    def logger_init(self) -> None:
        """ initialize the logger """
        # setup the logger
        logger.remove()
        self.sys_log_stdout_handler = logger.add(sys.stdout,
                                                 level=self.config.sys_log_level)
        if self.config.sys_log_save:
            output_dir = self.config.output_dir
            self.sys_log_save_handler = \
                logger.add(f"{output_dir}/syslog.log", rotation="10 MB",
                           level=self.config.sys_log_level
                           )

    def db_url(self, only_server=False) -> str:
        """ return the database url """
        if self.config.db.db_type == "sqlite":
            if self.config.output_dir is not None:
                sqlite_path = f"{self.config.output_dir}/{self.config.db.path}"
            else:
                sqlite_path = self.config.db.path
            return f"sqlite:///{sqlite_path}"
        elif self.config.db.db_type == "postgres":
            conn = self.config.db.connection
            server_connection = f"postgresql+psycopg2://"\
                   f"{conn['user']}:{conn['password']}@"\
                   f"{conn['host']}:{conn['port']}"
            if only_server:
                return server_connection
            else:
                return f"{server_connection}/{conn['name']}"

    #

    def init_db_connection(self) -> None:
        """ initialize the database """
        assert self.config.use_database, "use_database is False"
        db_url = self.db_url()
        logger.debug("Connecting to the database")
        self.db_engine = create_engine(db_url)


    def check_db_exists(self) -> None:
        return database_exists(self.db_engine.url)






