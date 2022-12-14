from pathlib import Path

from pyprojroot import here

_PATHS = {"config": "temperature_control/config.toml"}


def get_path(name: str) -> Path:
    return here(_PATHS[name])
