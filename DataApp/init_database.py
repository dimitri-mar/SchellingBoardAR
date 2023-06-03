""" this script create the database following  the configuration files """
from loguru import logger
from  DataApp.AppManager import AppManager
from DataManagement.MatchDatabase import Base


def init_db():
    logger.info("Initializing database")
    app_manager = AppManager()
    db_engine = app_manager.db_engine
    Base.metadata.create_all(db_engine)
    logger.info("Database initialized")





if __name__ == "__main__":
    init_db()







