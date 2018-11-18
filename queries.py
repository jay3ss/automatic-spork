"""Module containing the queries used"""
from contextlib import contextmanager
import logging

from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import exists

import config
from models import Definition


Session = sessionmaker(bind=config.engine)

logger = logging.getLogger('dictionaryapi.queries')


def create_new_definition(word, defns):
    """Creates a new word and definition in the database.

    :param word:    (str) word being defined
    :param defns:   (tuple) long definition, short definition
    """
    longdef, shortdef = defns
    definition = Definition(
        word=word, long_definition=longdef, short_definition=shortdef)
    with session_scope() as session:
        session.add(definition)


def update_definition(word, definition):
    """Updates the defintion of a word in the database

    :param word:    (str) word being defined
    :definition:    (tuple) long definition, short definition
    """
    longdef, shortdef = definition
    with session_scope() as session:
        defn = session.query(Definition).filter_by(word=word)
        defn.longdef = longdef
        defn.shortdef = shortdef


def is_in_database(word):
    """Determines if word exists in database.

    :param word:    (str) word being defined
    :return:        True if word is found in the database. Otherwise, False.
    """
    session = Session()
    does_exist = False
    try:
        does_exist = session.query(exists().where(
            Definition.word == word)).scalar()
    except:
        logger.error('An error occurred accessing the database', exc_info=True)
    finally:
        session.close()

    return does_exist


@contextmanager
def session_scope():
    """Provide a transactional scope around a series of operations.

    Taken from:

    https://docs.sqlalchemy.org/en/latest/orm/session_basics.html#when-do-i-construct-a-session-when-do-i-commit-it-and-when-do-i-close-it
    """
    session = Session()
    try:
        yield session
        session.commit()
    except:
        logger.error('An error occurred accessing the database', exc_info=True)
        session.rollback()
        raise
    finally:
        session.close()
