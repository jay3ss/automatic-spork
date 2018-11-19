# automatic-spork

Code to interact with the dictionary.com API. Just a start, nothing fancy.

## Getting started

This project relies on the following environment variables being set:
- `DICTIONARY_COM_API_KEY`
- `DICTIONARY_COM_LOGGING_LEVEL`
- `DICTIONARY_COM_SQL_STATEMENT_LEVEL`

I set these variables in a `.envrc` file, for example:

```bash
export DICTIONARY_COM_API_KEY=abc1234
export DICTIONARY_COM_LOGGING_LEVEL=DEBUG
export DICTIONARY_COM_SQL_STATEMENT_LEVEL=DEBUG
```

Both `DICTIONARY_COM_LOGGING_LEVEL` and `DICTIONARY_COM_SQL_STATEMENT_LEVEL` can take the either `DEBUG` or `PRODUCTION` as 
values which will log all `INFO` and above events, or all `WARNING` and above events, respectively. To get your API key for 
the site (the value of the `DICTIONARY_COM_API_KEY` environment variable) visit
[the dictionary.com API site](http://dictionaryapi.com/) and sign up for an account.

## Installation

This has been developed with Python 3.6.1, uses `sqlite` as the database, and depends on `requests` and `sqlalchemy`. You
can install them by running (preferably from a virtual environment)

```bash
pip install -r requirements.txt
```
And to build the databse, run

```bash
python build_database.py
```

## Running It

This can be used to grab the definition of a single word or a list of words (as shown in the `words.txt` file). To get the
definition of one word, run

```bash
python get_definitions.py one <word>
```

where `<word>` is the word you want to define. To get the definitions of words in a text file, run

```bash
python get_definitions.py from_file <words-list.txt>
```

where `<words-list.txt>` is your list of words. To save the definition(s) to the database, fir


The definitions can also optionally be saved using the `--save` flag
(e.g., `python get_definitions.py one <word> --save`). For help, use the `--help` flag 
(e.g., `python get_definitions.py --help`).
