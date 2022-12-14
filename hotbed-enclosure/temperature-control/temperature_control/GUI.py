from pathlib import Path

from PySide6.QtWidgets import (
    QMainWindow, QGroupBox, QHBoxLayout, QPushButton, QLabel, QVBoxLayout,
    QWidget, QFileDialog
)


class TempLogUtilsGUI(QMainWindow):
    def __init__(self):
        super().__init__()

        self._init_ui()

    def _init_ui(self) -> None:
        self._create_io_group_box()

        self.selected_file_path = QLabel(self.tr("Selected file: "))

        main_layout = QVBoxLayout()
        main_layout.addWidget(self._io_group_box)
        main_layout.addWidget(self.selected_file_path)
        self.setLayout(main_layout)

        self.setWindowTitle(self.tr("Temperature Logging Utilities"))

        # To have widgets appear.
        dummy_widget = QWidget()
        dummy_widget.setLayout(main_layout)
        self.setCentralWidget(dummy_widget)

    def _create_io_group_box(self) -> None:
        self._io_group_box = QGroupBox(self.tr("IO"))
        layout = QHBoxLayout()

        browse_button = QPushButton(self.tr("Browse"))
        browse_button.clicked.connect(self._browse_file)

        layout.addWidget(browse_button)

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
