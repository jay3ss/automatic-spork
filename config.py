"""Configuration of the project

The environment variables are set by the .envrc file
"""
import os

from sqlalchemy import create_engine


# Info from enivronment variables
api_key = os.environ.get('DICTIONARY_COM_API_KEY')
log_level = os.environ.get('DICTIONARY_COM_LOGGING_LEVEL', 'PRODUCTION')
sql_level = os.environ.get('DICTIONARY_COM_SQL_STATEMENT_LEVEL', 'PRODUCTION')
log_filename = os.environ.get('DICTIONARY_COM_LOG_FILE', 'dictionaryapi.log')

basedir = os.path.abspath(os.path.dirname(__file__))
db_url = 'sqlite:////' + os.path.join(basedir, 'definitions.db')

# Connect to the database. Default is to not echo everything to the terminal
if sql_level == 'DEBUG':
    echo = True
else:
    echo = False
engine = create_engine(db_url, echo=echo)

# Logging setup and configuration
# LOGGER_NAME = 'DictApiLogger'
# LEVELS = {
#     'DEBUG': logging.DEBUG,
#     'PRODUCTION': logging.WARNING
# }
# logging_level = LEVELS[log_level]
# # logger = logging.getLogger(LOGGER_NAME)
# logger = logging.getLogger(__name__)

# # Disable extra loggers

# logger.setLevel(logging_level)
# handler = logging.handlers.RotatingFileHandler(
#     log_filename,
#     maxBytes=10280,
#     backupCount=20,
# )
# logger.addHandler(handler)
