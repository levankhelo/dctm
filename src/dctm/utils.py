from logging import error
import json, yaml;


def load_config(config_file):
    """Transform json or yaml to dictionary

    Args:
        config_file (string): path to config file

    Returns:
        dict: json or yaml converted to dictionary
    """
    with open(config_file, "r") as file:
        config = file.read()

    config_dict = dict()
    valid_json = True
    valid_yaml = True

    try:
        config_dict = json.loads(config)
    except:
        print("Error trying to load the config file in JSON format")
        valid_json = False

    try:
        config_dict = yaml.safe_load(config)
        print("Error trying to load the config file in YAML format")
    except:
        print("Error trying to load the config file in YAML format")
        valid_yaml = False
    return config_dict
