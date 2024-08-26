import os

import toml

# prevent relative path error
current_dir = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(current_dir, "config.toml")

try:
    with open(config_path) as file:
        CONFIG = toml.load(file)
except FileNotFoundError:
    raise FileNotFoundError("Please provide a toml file")
