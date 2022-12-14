from sys import exit

from PySide6.QtWidgets import QApplication

from GUI import TempLogUtilsGUI

if __name__ == "__main__":
    app = QApplication([])

    window = TempLogUtilsGUI()
    window.resize(400, 400)
    window.show()

    exit(app.exec())
