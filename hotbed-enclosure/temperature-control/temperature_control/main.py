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

    RELATIVE_PATHS = False

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
