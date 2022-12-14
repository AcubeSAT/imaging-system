from sys import exit

from PySide6.QtWidgets import QApplication

from GUI import TempLogUtilsGUI
from IOUtils import read_config
from paths import get_path

if __name__ == "__main__":
    RELATIVE_PATHS = True

    CONFIG = read_config(get_path("config", RELATIVE_PATHS))
    WINDOW_CONFIG = CONFIG.window

    app = QApplication([])

    window = TempLogUtilsGUI()
    window.resize(
        WINDOW_CONFIG["dimension"]["width"],
        WINDOW_CONFIG["dimension"]["height"]
    )
    window.show()

    exit(app.exec())
