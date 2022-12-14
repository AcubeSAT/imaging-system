from pathlib import Path
from tomllib import load


def _read_toml(filename: Path):
    with open(filename, mode = 'rb') as fp:
        config = load(fp)
    return config
