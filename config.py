from configparser import ConfigParser, ParsingError
import os
import openai

class ConfigError(Exception):
    """
    Raised when an error occur while reading the config file.
    :param msg: Error message.
    """
    def __init__(self, msg: str):
        self.message = "Error in config file: " + msg
        super().__init__(self.message)

class MissingConfig(Exception):
    """
    Raised when a config value is missing.
    :param msg: Error message.
    """
    def __init__(self, msg: str):
        self.message = "Missing config value: " + msg
        super().__init__(self.message)


## DYNAMIC PARAMETERS:
# (pulled from the config file)

DJANGO_KEY = None

#: Contains database parameters.
DATABASE = {
    "host": "",
    "port": "",
    "name": "",
    "user": "",
    "password": "",
}


def get_config():
    """
    Populate the config data from the config file.
    """
    file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.cfg")

    if not os.path.isfile(file):
        raise ConfigError(f"{file} not found! "+file)


    config = ConfigParser(inline_comment_prefixes="#")
    try:
        config.read(file)
    except ParsingError as e:
        raise ConfigError(f"Parsing Error in '{file}'\n{e}")

    _check_section(config, "General", file)

    global DJANGO_KEY
    try:
        DJANGO_KEY = config["General"]["django_key"]
    except KeyError:
        _error_missing(DJANGO_KEY, 'General', file)
    except ValueError:
        _error_incorrect(DJANGO_KEY, 'General', file)

    _check_section(config, "Database", file)

    global DATABASE
    for key in DATABASE.keys():
        try:
            DATABASE[key] = config["Database"][key]
        except KeyError:
            _error_missing(key, 'Database', file)
        except ValueError:
            _error_incorrect(key, 'Database', file)

    _check_section(config, "OpenAI", file)
    try:
        openai.organization = config["OpenAI"]["org_id"]
    except KeyError:
        _error_missing("org_id", 'OpenAI', file)
    except ValueError:
        _error_incorrect("org_id", 'OpenAI', file)

    try:
        openai.api_key = config["OpenAI"]["api_key"]
    except KeyError:
        _error_missing("api_key", 'OpenAI', file)
    except ValueError:
        _error_incorrect("api_key", 'OpenAI', file)

def _check_section(config, section, file):
    if section not in config:
        raise ConfigError(f"Missing section '{section}' in '{file}'")


def _error_missing(field, section, file):
    raise ConfigError(f"Missing field '{field}' in '{section}' in '{file}'")


def _error_incorrect(field, section, file):
    raise ConfigError(f"Incorrect field '{field}' in '{section}' in '{file}'")