"""Module to interact with the dictionary.com API

Make sure to source .envrc, otherwise, a JSONDecodeError will occur
"""
import logging

import requests

from config import api_key


logger = logging.getLogger('dictionaryapi.dictionary')


def get_word_json(word):
    """Queries the dictionary.com API for a particular word and returns the
    JSON response if the word is spelled correctly. Otherwise, a
    SpellingException is raised.
    """
    url = ('https://www.dictionaryapi.com/api/v3/references/'
           f'collegiate/json/{word}?key={api_key}')
    try:
        resp = requests.get(url=url)

        # A 200 status code always seems to be returned, even if an empty API
        # key is used (although the response isn't JSON). Therefore, no need
        # to check the status code.
        # TODO: check for errors/exceptions?
        if isinstance(resp.json()[0], dict):
            return resp.json()[0]

    except:
        error_msg = ('Error has occurred while attempting '
                     f'to get the definition for "{word}"')
        logger.error(error_msg, exc_info=True)
        raise SpellingException(f'The word "{word}" was spelled incorrectly')


def extract_shortdef(resp):
    """Extracts the short definition of a word from the JSON response

    Words with more than one definition have a list of each definition returned
    by the API. Therefore, each definition is join()ed to a single string with
    a \n as the separator.

    :param resp:    (JSON) response from the dictionary.com API
    """
    try:
        return '\n'.join(resp['shortdef'])
    except (KeyError, TypeError) as err:
        logger.error(err, exc_info=True)


def extract_longdef(resp):
    """Extracts the short definition of a word from the JSON response

    :param resp:    (JSON) response from the dictionary.com API
    """
    try:
        return resp['def'][0]['sseq'][0][0][1]['dt'][0][1]
    except (KeyError, TypeError) as err:
        logger.error('Couldn\'t extract long definition')
        logger.error(err)


class SpellingException(Exception):
    """For misspelled words"""
    pass
