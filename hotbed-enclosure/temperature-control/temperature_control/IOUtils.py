from pathlib import Path
from tomllib import load

from pandas import DataFrame, read_csv

from config_model import Config
from eltypes import config, config_model, log_data


def _read_csv(filename: Path) -> DataFrame:
    return read_csv(filename, sep=',')


def read_file(filename: Path) -> log_data:
    return _read_csv(filename)


def _read_toml(filename: Path) -> config:
    with open(filename, mode='rb') as fp:
        config = load(fp)
    return config


def read_config(filename: Path) -> config_model:
    conf_from_file = _read_toml(filename)
    return Config.parse_obj(conf_from_file)
