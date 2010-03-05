import MySQLdb
import logging
import logging.handlers
import admininfo


def init_log(name):
    """Method to initialise logger module - refer to python library for better
    explanation on logging module"""
    
    LOG_FILE_NAME = admininfo.log_file_name
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    handler = logging.handlers.RotatingFileHandler(LOG_FILE_NAME, maxBytes = 2000000)
    logger.addHandler(handler)

    return logger
               



def init_db():
    """Method to initialise DB connections"""
    
    host = admininfo.auth_dict['db-host']
    
    user = admininfo.auth_dict['db-user']

    passwd = admininfo.auth_dict['db-pass']

    db = admininfo.auth_dict['db-name']

    
    #creates a database object for corresponding config

    db=MySQLdb.connect(host,user,passwd,db)

    cursor=db.cursor()

    return cursor
