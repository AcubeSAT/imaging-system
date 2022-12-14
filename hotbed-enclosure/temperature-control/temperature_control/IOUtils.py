from pathlib import Path
from tomllib import load

from pandas import DataFrame, read_csv

from config_model import Config
from eltypes import config, config_model, csv_format, log_data, markdown_format


def _read_csv(filename: Path) -> DataFrame:
    return read_csv(filename, sep=',')


def read_file(filename: Path) -> log_data:
    DATA_HEADER = ["Reading", "Temperature", "Humidity"]

    df = _read_csv(filename)
    df.columns = DATA_HEADER
    return df


def _read_toml(filename: Path) -> config:
    with open(filename, mode='rb') as fp:
        config = load(fp)
    return config


def read_config(filename: Path) -> config_model:
    conf_from_file = _read_toml(filename)
    return Config.parse_obj(conf_from_file)


def _data_to_markdown(data: DataFrame) -> markdown_format:
    return data.to_markdown(index=False, numalign="left")


def _data_to_csv(data: DataFrame) -> csv_format:
    return data.to_csv(index=False)
