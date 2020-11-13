import platform
import yaml

debugging = "macOS" in platform.platform()
interval = 60 if debugging else 240

with open("clock_config.yaml", 'r') as stream:
    try:
        CLOCK = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        CLOCK = None
