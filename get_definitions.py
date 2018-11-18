"""Gets the definition for the words in the file passed as an argument to
this script
"""
import argparse
import logging

import config
import dictionary
import queries


# Logging setup and configuration
LEVELS = {
    'DEBUG': logging.DEBUG,
    'PRODUCTION': logging.WARNING
}
LOG_FORMAT = ('%(levelname)s - %(asctime)s - %(name)s - '
              '%(funcName)s:%(lineno)d - %(message)s')
FORMATTER = logging.Formatter(LOG_FORMAT)
logging_level = LEVELS[config.log_level]
logger = logging.getLogger('dictionaryapi')

logger.setLevel(logging_level)
handler = logging.handlers.RotatingFileHandler(
    config.log_filename,
    maxBytes=1024,
    backupCount=20,
)
handler.setFormatter(FORMATTER)
logger.addHandler(handler)


def get_definitions(resp):
    """Gets the long and short definitions of a response from the
    dictionary.com API and returns them as a tuple

    :param resp:    (JSON) response from the dictionary.com API
    :return:        (tuple) long and short definitions of the word
    """
    longdef = dictionary.extract_longdef(resp)
    shortdef = dictionary.extract_shortdef(resp)
    return (longdef, shortdef)


def one(arg):
    """Get the definition for one word. Callback used by argparser for the
    'one' argument

    :param arg: commandline argument
    """
    word = arg.word
    try:
        resp = dictionary.get_word_json(word)
        longdef, shortdef = get_definitions(resp)

        if config.log_level:
            logger.info('%s\n\n', word.upper())
            logger.info('Long definition:\n%s\n', longdef)
            logger.info('Short definition(s):\n%s\n', shortdef)

        if arg.save:
            insert_to_database((word, longdef, shortdef))

    except (dictionary.SpellingException, KeyError) as err:
        logger.error(err, exc_info=True)
        logger.error('Something went wrong trying to define "%s"', word)


def from_file(arg):
    """Get the definition of words from a file that is specified. Callback
    used by argparser

    :param arg: commandline argument
    """
    with open(arg.file_name, 'r') as f:
        words = f.read()

    words = words.split('\n')

    for word in words:
        resp = dictionary.get_word_json(word)
        longdef, shortdef = get_definitions(resp)
        if arg.save:
            insert_to_database((word, longdef, shortdef))



def insert_to_database(definition):
    """Checks if a definition exists. If it does, it updates the database
    entry. Otherwise, it creates a new definition and saves it to the
    database.

    :param definition:  (tuple) word and its long and short definitions,
                        respectively
    """
    word, longdef, shortdef = definition
    if queries.is_in_database(word):
        logger.info('"%s"\'s definition has been updated', word)
        queries.update_definition(word, (longdef, shortdef))
    else:
        logger.info('"%s"\'s definition has been created', word)
        queries.create_new_definition(word, (longdef, shortdef))


parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers()

# For one word
one_parser = subparsers.add_parser('one')
one_parser.add_argument('word')
one_parser.set_defaults(func=one)

# From a file
from_file_parser = subparsers.add_parser('from_file')
from_file_parser.add_argument('file_name')
from_file_parser.set_defaults(func=from_file)

# Flags
parser.add_argument('--save', action="store_true", default=False)


if __name__ == '__main__':
    args = parser.parse_args()
    args.func(args)
