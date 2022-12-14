<div align="center">
<p>
    <a href="https://benchling.com/organizations/acubesat/">Benchling 🎐🧬</a> &bull;
    <a href="https://gitlab.com/acubesat/documentation/cdr-public/-/blob/master/DDJF/DDJF_PL.pdf?expanded=true&viewer=rich">DDJF_PL 📚🧪</a> &bull;
    <a href="https://spacedot.gr/">SpaceDot 🌌🪐</a> &bull;
    <a href="https://acubesat.spacedot.gr/">AcubeSAT 🛰️🌎</a>
</p>
</div>

## Description

Here's some code to help automate the following:

- generation of useful formats out of experimental raw data (CSV for programmatic work, Markdown for quick inspection, plots)
- proper data indexing/organization

You can get a bundle for your OS from the [releases](https://github.com/AcubeSAT/imaging-system/releases/tag/v0.1.0-alpha) page.

## Table of Contents

<details>
<summary>Click to expand</summary>

- [Description](#description)
- [Table of Contents](#table-of-contents)
- [DHT Temperature Control Utilities](#dht-temperature-control-utilities)
  - [Description](#description-1)
  - [File Structure](#file-structure)
    - [CI](#ci)
    - [Source](#source)
    - [Dependencies](#dependencies)
    - [Rest](#rest)

</details>

## DHT Temperature Control Utilities

### Description

A cross-platform GUI bundled as an executable to help quickly generate raw data captured by a DHT temperature/humidity ambient sensor.

![Example screenshot](https://github.com/AcubeSAT/imaging-system/blob/main/hotbed-enclosure/temperature-control/assets/screenshot.png)

1. Click on `Browse`
2. Load the data
3. Click on `Export`
4. A directory inside `logs/` will have been generated, with a CSV, Markdown table, and plot with the original filename and the respective suffixes (see `example-data/`)
5. Upload the data somewhere
6. ???
7. Profit

### File Structure

<details>
<summary>Click to expand</summary>

```graphql
./.github/workflows
└─ ci.yml
./arduino/
├─ DHT.h
└─ temperature-sensor.ino
./src/
├─ config_model.py
├─ config.toml
├─ eltypes.py
├─ GUI.py
├─ IOUtils.py
├─ main.py
├─ operators.py
├─ paths.py
└─ plot.py
.editorconfig
add-files-to-spec
poetry.lock
poetry.toml
pyproject.toml
```

</details>

#### CI

All [CI magic](https://github.com/AcubeSAT/imaging-system/actions/workflows/ci.yml) happens using [GitHub Actions](https://docs.github.com/en/actions).
The related configuration is all located within `.github/workflows/ci.yml`:

<details>
<summary>Click to expand</summary>

```yaml
name: CI
run-name: ${{ github.actor }} is running 🚀
on: [push] # Triggered by push.

jobs:
  ci:
    strategy:
      fail-fast: false # Don't fail all jobs if a single job fails.
      matrix:
        python-version: ["3.11"]
        poetry-version: ["1.2.2"] # Poetry is used for project/dependency management.
        os: [ubuntu-latest, macos-latest, windows-latest]
        include: # Where pip stores its cache is OS-dependent.
          - pip-cache-path: ~/.cache
            os: ubuntu-latest
          - pip-cache-path: ~/.cache
            os: macos-latest
          - pip-cache-path: ~\appdata\local\pip\cache
            os: windows-latest
    defaults:
      run:
        shell: bash # For sane consistent scripting throughout.
        working-directory: ./hotbed-enclosure/temperature-control
    runs-on: ${{ matrix.os }} # For each OS:
    steps:
      - name: Check out repository
        uses: actions/checkout@v3
      - name: Setup Python
        id: setup-python
        uses: actions/setup-python@v4
        with:
          python-version: ${{ matrix.python-version }}
      - name: Install Poetry
        uses: snok/install-poetry@v1
        with:
          version: ${{ matrix.poetry-version }}
          virtualenvs-create: true
          virtualenvs-in-project: true # Otherwise the venv will be the same across all OSes.
          installer-parallel: true
      - name: Load cached venv
        id: cached-pip-wheels
        uses: actions/cache@v3
        with:
          path: ${{ matrix.pip-cache-path }}
          key: venv-${{ runner.os }}-${{ steps.setup-python.outputs.python-version }}-${{ hashFiles('**/poetry.lock') }}
      - name: Install dependencies
        run: poetry install --no-interaction --no-root -E build -E format # https://github.com/python-poetry/poetry/issues/1227
      - name: Check formatting
        run: |
          source $VENV
          yapf -drp --no-local-style --style "facebook" temperature_control/
      - name: Build for ${{ matrix.os }}
        run: | # https://stackoverflow.com/questions/19456518/error-when-using-sed-with-find-command-on-os-x-invalid-command-code
          source $VENV
          pyi-makespec temperature_control/main.py
          if [ "$RUNNER_OS" == "macOS" ]; then
            sed -i '' -e '2 r add-files-to-spec' main.spec
            sed -i '' -e 's/datas=\[]/datas=added_files/' main.spec
          else
            sed -i '2 r add-files-to-spec' main.spec
            sed -i 's/datas=\[]/datas=added_files/' main.spec
          fi
          pyinstaller main.spec
      - name: Archive binary artifacts
        uses: actions/upload-artifact@v3
        with:
          name: ${{ matrix.os }}-bundle
          path: ./hotbed-enclosure/temperature-control/dist
```

</details>

On each push, the application is bundled into a single folder containing an executable, for each OS.
This happens using [`pyinstaller`](https://www.pyinstaller.org/).
First there's a formatting check using [`yapf`](https://github.com/google/yapf).
Then, the application is built.
`pytest` is included as an extra optional dependency to add unit test support in the future.
Everything is cached when possible.
If the job terminates successfully, the bundle folder for each OS is uploaded as an [artifact](https://github.com/AcubeSAT/imaging-system/actions/runs/3692814721) that the user can download, instead of having to run `pyinstaller` locally, or having to install `python` and the project dependencies locally through `poetry`.

#### Source

`main.py` is the entrypoint to be run:

<details>
<summary>Click to expand</summary>

```python
import logging
from sys import exit

from PySide6.QtWidgets import QApplication
# Yes, tabulate is unused here.
# However, it's an optional dependency of pandas
# needed to convert a DataFrame to a markdown table
# and I didn't find any other way to tell pyinstaller
# that it has to bundle tabulate too.
# So keep this line.
import tabulate

from GUI import TempLogUtilsGUI
from IOUtils import read_config
from paths import get_path

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%d-%b-%y %H:%M:%S'
    )
    logging.info("Logger initialized.")

    RELATIVE_PATHS = True

    CONFIG = read_config(get_path("config", RELATIVE_PATHS))
    if not CONFIG:
        logging.error("Loading the configuration file failed.")
        exit(1)
    logging.info("Configuration file loaded successfully.")

    WINDOW_CONFIG = CONFIG.window
    PLOT_CONFIG = CONFIG.plot

    app = QApplication([])

    logging.info("Starting main window.")
    window = TempLogUtilsGUI(PLOT_CONFIG, RELATIVE_PATHS)
    window.resize(
        WINDOW_CONFIG["dimension"]["width"],
        WINDOW_CONFIG["dimension"]["height"]
    )
    window.show()
    logging.info("Window rendered successfully.")

    EXIT_CODE = app.exec()

    close_msg = "App exited successfully." if not EXIT_CODE else "App crashed."
    logging.info(close_msg)

    exit(EXIT_CODE)
```

</details>

It creates the GUI (using [`PySide6`](https://pypi.org/project/PySide6/)) main application.
Configuration for the GUI is stored in a separate [TOML](https://github.com/toml-lang/toml) file, `config.toml`.
The config model is verified using [`pydantic`](https://pydantic-docs.helpmanual.io/).

---

The GUI is the backbone of the application, and it's described in `GUI.py`:

<details>
<summary>Click to expand</summary>

```python
import logging
from pathlib import Path

from PySide6.QtWidgets import (
    QMainWindow, QGroupBox, QHBoxLayout, QPushButton, QLabel, QVBoxLayout,
    QWidget, QFileDialog, QPlainTextEdit
)

from eltypes import config
from IOUtils import data_to_markdown, data_to_csv, read_file, write_to_file
from paths import get_path
from plot import plot


class TempLogUtilsGUI(QMainWindow):
    def __init__(self, plot_config: config, relative_paths: bool):
        super().__init__()

        self.plot_config = plot_config
        self.relative_paths = relative_paths

        self._init_ui()

    def _init_ui(self) -> None:
        self._create_io_group_box()

        self.selected_file_path = QLabel(self.tr("Selected file: "))

        self.data_viewer = QPlainTextEdit()
        self.data_viewer.setReadOnly(True)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self._io_group_box)
        main_layout.addWidget(self.selected_file_path)
        main_layout.addWidget(self.data_viewer)
        self.setLayout(main_layout)

        self.setWindowTitle(self.tr("Temperature Logging Utilities"))

        # To have widgets appear.
        dummy_widget = QWidget()
        dummy_widget.setLayout(main_layout)
        self.setCentralWidget(dummy_widget)

        self.selected_file = None
        self.data = None

        logging.info("UI initialized successfully.")

    def _create_io_group_box(self) -> None:
        self._io_group_box = QGroupBox(self.tr("IO"))
        layout = QHBoxLayout()

        browse_button = QPushButton(self.tr("Browse"))
        browse_button.clicked.connect(self._browse_file)

        export_button = QPushButton(self.tr("Export"))
        export_button.clicked.connect(self._export_file)

        layout.addWidget(browse_button)
        layout.addWidget(export_button)

        self._io_group_box.setLayout(layout)

    def _browse_file(self) -> None:
        dialog = QFileDialog(self)
        dialog.setFileMode(QFileDialog.ExistingFile)
        dialog.setViewMode(QFileDialog.List)

        if dialog.exec():
            filename = dialog.selectedFiles()[0]
            filename = Path(filename)

            self.selected_file_path.setText(
                self.tr(f"Selected File: {filename.name}")
            )

            self.selected_file = filename
            self.data = read_file(filename)

            self._update_data_viewer()

            logging.info(f"Loaded file {filename.name} successfully.")

    def _export_file(self) -> None:
        def _export_data_kind(data_type: str, filename: Path) -> None:
            filename = filename.with_suffix(data_type)
            data = data_to_csv(
                self.data
            ) if data_type == ".csv" else data_to_markdown(self.data)

            write_to_file(data, filename)

        if self.data is None:
            return None

        source = self.selected_file.name

        target = get_path("logs", self.relative_paths) / source
        target.mkdir(parents=True, exist_ok=True)

        filename = target / "data"
        for extension in (".csv", ".md"):
            _export_data_kind(extension, filename)

        dimensions = (
            self.plot_config["dimension"]["width"],
            self.plot_config["dimension"]["height"]
        )
        plot(self.data, filename.with_suffix(".png"), dimensions)

        logging.info(f"Exported from file {source} successfully.")

    def _update_data_viewer(self) -> None:
        if self.data is not None:
            self.data_viewer.setPlainText(self.data.to_string(index=False))
```

</details>

Essentially, there's:

- Various buttons
- A reader

A datafile can be loaded into the app through the `Browse` button, and exported through the `Export` button, respectively.
After a file is loaded, its filename is logged and its content is put in the reader for the user to browse.

The reader supports the following keybinds:

| Keybind | Description |
| ------- | ----------- |
| `UpArrow` | Moves one line up |
| `DownArrow` | Moves one line down |
| `LeftArrow` | Moves one character to the left |
| `RightArrow` | Moves one character to the right |
| `PageUp` | Moves one (viewport) page up |
| `PageDown` | Moves one (viewport) page down |
| `Home` | Moves to the beginning of the G-Code |
| `End` | Moves to the end of the G-Code |
| `Alt+Wheel` | Scrolls the page horizontally |
| `Ctrl+Wheel` | Zooms the G-Code |
| `Ctrl+A` | Selects all text |

---

`plot.py` holds the code for generating a plot out of the parsed DHT data.
It primarily uses [seaborn](https://seaborn.pydata.org/):

<details>
<summary>Click to expand</summary>

```python
from pathlib import Path

import matplotlib.pyplot as plt
import seaborn as sns

from eltypes import log_data, plot_dimensions


def plot(data: log_data, filename: Path, dimensions: plot_dimensions) -> None:
    sns.set_theme("talk", "darkgrid")
    current_palette = sns.color_palette("bright")

    WIDTH, HEIGHT = dimensions
    _, (ax1, ax2) = plt.subplots(1, 2, figsize=(WIDTH, HEIGHT))

    temperature_series = data.iloc[:, 1]
    humidity_series = data.iloc[:, 2]

    sns.lineplot(
        data=temperature_series,
        ax=ax1,
        drawstyle="steps-pre",
        color=current_palette[0]
    )
    sns.lineplot(
        data=humidity_series,
        ax=ax2,
        drawstyle="steps-pre",
        color=current_palette[1]
    )

    plt.savefig(filename)
```

</details>

---

`eltypes.py` is for creating custom types for better [type hints](https://docs.python.org/3/library/typing.html), as well as grouping all types in a single source file:

<details>
<summary>Click to expand</summary>

```python
from pandas import DataFrame

from config_model import Config

config = dict
config_model = Config

log_data = DataFrame

csv_format = str
markdown_format = str

plot_dimensions = tuple[int, int]
```

</details>

---

Respectively, `paths.py` holds all (assets & config) paths:

<details>
<summary>Click to expand</summary>

```python
from pathlib import Path

from pyprojroot import here

_PATHS = {"config": "temperature_control/config.toml", "logs": "logs/"}


def get_path(name: str, relative: bool) -> Path:
    return here(_PATHS[name]) if not relative else _PATHS[name]
```

</details>

[`pathlib`](https://docs.python.org/3/library/pathlib.html) is used for sane path handling across OSes.
[`pyprojroot`](https://github.com/chendaniely/pyprojroot) is used to locate the project root to better handle absolute paths.
It's akin to [`rprojroot`](https://github.com/r-lib/rprojroot) or [`here`](https://here.r-lib.org/).
*Note*: absolute paths can't be used to build the application, since we want it to be distributable and able to work regardless of the directory it's located in; therefore relative paths are used instead.
However, absolute paths with `pyprojroot` can help a lot during development - refer to `relative_paths = True` in `main.py`.

---

`config_model.py` holds the `pydantic` `BaseModel` representation of the application configuration:

```python
from pydantic import BaseModel


class Config(BaseModel):
    window: dict[str, dict[str, int]]
    plot: dict[str, dict[str, int]]
```

---

Finally, `config.toml`, the (editable) configuration file:

<details>
<summary>Click to expand</summary>

```toml
[window]

    [window.dimension]
    width = 600
    height = 700

[plot]

    [plot.dimension]
    width = 15
    height = 7
```

</details>

#### Dependencies

Project and dependency management happens through `poetry`:

<details>
<summary>Click to expand</summary>

```toml
[tool.poetry]
name = "temperature-control"
version = "0.1.0"
description = "Python utilities to log and index temperature sensor readings."
authors = ["Orestis Ousoultzoglou <orousoultzoglou@gmail.com>"]
license = "MIT"
readme = "README.md"
packages = [ { include = "temperature_control" } ]

[tool.poetry.dependencies]
python = "~3.11"
pytest = { version = "^7.2.0", optional = true }
yapf = { version = "^0.32.0", optional = true }
pyside6 = "^6.4.1"
toml = { version = "^0.10.2", optional = true }
pydantic = "^1.10.2"
pyprojroot = "^0.2.0"
pandas = "^1.5.2"
tabulate = "^0.9.0"
seaborn = "^0.12.1"
matplotlib = "^3.6.2"
pyinstaller = { version = "^5.7.0", optional = true }

[tool.poetry.extras]
build = ["pyinstaller"]
format = ["yapf", "toml"]
test = ["pytest"]

[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"
```

</details>

- [`pyside6`](https://pypi.org/project/PySide6/): `PySide6` is the official Python module from the Qt for Python project, which provides access to the complete Qt 6.0+ framework. Used for the GUI
- [`pyprojroot`](https://pypi.org/project/pyprojroot/): Find relative paths from a project root directory. Used for making my life better during development
- [`pydantic`](https://pypi.org/project/pydantic/): Data validation and settings management using Python type hints. Used for validating the configuration TOML

Some [clusters of optional dependencies](https://python-poetry.org/docs/pyproject/#extras) have also been added.
These aren't required for the application to run.
These clusters are:

- `build`: [`pyinstaller`](https://pypi.org/project/pyinstaller/): PyInstaller bundles a Python application and all its dependencies into a single package. Used for bundling the application into a single folder with an executable
- `format`:
  - [`yapf`](https://pypi.org/project/yapf/): A formatter for Python files. Used for, well, you guessed it. Also used in CI
  - [`toml`](https://pypi.org/project/toml/): A Python library for parsing and creating TOML. *Not* used for parsing the config file. It's required from `yapf`
- `test`: [`pytest`](https://pypi.org/project/pytest/): The `pytest` framework makes it easy to write small tests, yet scales to support complex functional testing for applications and libraries. Can be used to set up unit testing some time in the future

#### Rest

- `add-files-to-spec` is a clever hack to add [the data files to be bundled](https://pyinstaller.org/en/stable/spec-files.html) to the `pyinstaller` `spec` generated files through `sed`
- `.editorconfig` is [cool](https://editorconfig.org/)
