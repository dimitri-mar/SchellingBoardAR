""" this script create the database following  the configuration files """
from loguru import logger
from  DataApp.AppManager import AppManager
from DataManagement.MatchDatabase import Base


def init_db():
    logger.info("Initializing database")
    app_manager = AppManager()
    logger.debug(f"app_manager: {app_manager} is going to create initialize the database"
                 f" with db_engine: {app_manager.db_engine}\n"
                 "with the following configurations:\n"
                f"db_path: {app_manager.config.db}\n"
                 )

    app_manager.init_db_connection()
    db_engine = app_manager.db_engine
    logger.debug(f"db_engine: {db_engine}")

    Base.metadata.create_all(db_engine)
    logger.info("Database initialized")





if __name__ == "__main__":
    init_db()







