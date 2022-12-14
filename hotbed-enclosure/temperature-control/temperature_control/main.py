from sys import exit

from PySide6.QtWidgets import QApplication

from GUI import TempLogUtilsGUI
from IOUtils import read_config

if __name__ == "__main__":
    CONFIG = read_config('config.toml')
    WINDOW_CONFIG = CONFIG.window

    app = QApplication([])

    window = TempLogUtilsGUI()
    window.resize(
        WINDOW_CONFIG["dimension"]["width"],
        WINDOW_CONFIG["dimension"]["height"]
    )
    window.show()

    exit(app.exec())
