import os
from pathlib import Path

import yaml

THUMBNAIL_DIRECTORY_PATH = 'thumbnail/'

def _get_config():
    BASE_DIR = str(Path(__file__).resolve().parent.parent)
    with open(os.path.join(BASE_DIR, 'config.yml')) as f:
        config = yaml.safe_load(f,)
    config['BASE_DIR'] = BASE_DIR

    if os.path.exists(config['INVITION_CONFIG'].replace('BASE_DIR', BASE_DIR)):
        with open(config['INVITION_CONFIG'].replace('BASE_DIR', BASE_DIR)) as f:
            config.update(yaml.load(f, yaml.SafeLoader) or {})

    return config

CONFIG = _get_config()