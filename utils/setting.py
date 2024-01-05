import configparser
import pathlib

def get_settings():
    config_path = pathlib.Path(__file__).parent.absolute() / "config.ini"

    config = configparser.ConfigParser()

    config.read(config_path)


    settings = {
        'linkedin_logging_credentials': {
            'user': config['loggin_credentials']['user'],
            'password': config['loggin_credentials']['password']
        }
        }

    return settings
