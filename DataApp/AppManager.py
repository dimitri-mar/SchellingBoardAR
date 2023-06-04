from sqlalchemy import create_engine
from sqlalchemy_utils.functions import database_exists

from DataApp.ConfigManager import Config
from DataManagement.MatchDatabase import Match
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
        self.sys_log_stdout_handler= logger.add(sys.stdout,
                                                level=self.config.sys_log_level)
        if self.config.sys_log_save:
            output_dir = self.config.output_dir
            self.sys_log_save_handler = \
                logger.add(f"{output_dir}/syslog.log", rotation="10 MB",
                           level=self.config.sys_log_level
                           )
    def db_url(self)->str:
        """ return the database url """
        if self.config.db.db_type == "sqlite":
            if self.config.output_dir is not None:
                sqlite_path = f"{self.config.output_dir}/{self.config.db.path}"
            else:
                sqlite_path = self.config.db.path
            return f"sqlite:///{sqlite_path}"
        elif self.config.db.db_type == "postgres":
            conn = self.config.db.connection
            return f"postgresql+psycopg2://{conn['user']}:{conn['password']}@{conn['host']}:{conn['port']}/{conn['name']}"
    #



    def init_db_connection(self):
        """ initialize the database """
        assert self.config.use_database, "use_database is False"
        db_url = self.db_url()


        logger.debug("Connecting to the database")
        self.db_engine = create_engine(db_url )
        try:
            self.db_engine.connect()
        except Exception as e:
            logger.error(f"Error connecting to the database: {e}")
            logger.debug(f"the configuration was: {self.config.db}")
            sys.exit(1)

        #return db_engine
        # check if the database exists
        # if not raise exception if exsist do nothing









