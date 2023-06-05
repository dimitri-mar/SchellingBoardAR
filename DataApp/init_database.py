""" this script create the database following  the configuration files """
from loguru import logger
from sqlalchemy_utils import database_exists, create_database, drop_database

from  DataApp.AppManager import AppManager

from DataManagement.MatchDatabase import Base


def init_db():
    """ initialize the database """
    logger.info("Initializing database")
    app_manager = AppManager()
    logger.debug(f"app_manager: {app_manager} is going to create initialize the database"
                 f" with db_engine: {app_manager.db_engine}\n"
                 "with the following configurations:\n"
                f"db_path: {app_manager.config.db}\n"
                 )

    if not database_exists(app_manager.db_url()):
        logger.info("Database does not exist, creating it")
        create_database(app_manager.db_url())
        logger.info("Database created")
    else:
        logger.info("Database already exists")
        drop_it = input("Do you want to delete it? (y/n)")
        if drop_it == "y":
            if not input("Are you sure? This will delete the entire database (y/n)") == "y":
                logger.info("Database not deleted")
                return
            logger.info("Deleting database")
            drop_database(app_manager.db_url())
            create_database(app_manager.db_url())
            logger.info("Database deleted")

    app_manager.init_db_connection()
    db_engine = app_manager.db_engine
    logger.debug(f"db_engine: {db_engine}")

    Base.metadata.create_all(db_engine)
    logger.info("Database initialized")





if __name__ == "__main__":
    init_db()







