from pathlib import Path

from pyprojroot import here

_PATHS = {"config": "temperature_control/config.toml", "logs": "logs/"}


def get_path(name: str, relative: bool) -> Path:
    return here(_PATHS[name]) if not relative else _PATHS[name]
