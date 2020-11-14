import platform
import os
import yaml

debugging = "macOS" in platform.platform() or ("WEASLEY_DEBUG" in os.environ and os.environ["WEASLEY_DEBUG"] == "DEBUG")
interval = 60 if debugging else 240

with open("clock_config.yaml", 'r') as stream:
    try:
        CLOCK = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        CLOCK = None
