import yaml
import os

def get_config(env):
    with open(os.path.dirname(__file__) + '/base.yml', 'r') as base_file:
        base_config = yaml.safe_load(base_file)

    with open(os.path.dirname(__file__) + f'/{env}.yml', 'r') as env_file:
        env_config = yaml.safe_load(env_file)

    return base_config | env_config
