import logging
from pathlib import Path

from PySide6.QtWidgets import (
    QMainWindow, QGroupBox, QHBoxLayout, QPushButton, QLabel, QVBoxLayout,
    QWidget, QFileDialog, QPlainTextEdit
)

from IOUtils import data_to_markdown, data_to_csv, read_file, write_to_file
from paths import get_path


class TempLogUtilsGUI(QMainWindow):
    def __init__(self, relative_paths: bool):
        super().__init__()

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

        for extension in (".csv", ".md"):
            filename = get_path(
                "logs", self.relative_paths
            ) / self.selected_file.name

            _export_data_kind(extension, filename)
            logging.info(f"Exported from file {filename.name} successfully.")

    def _update_data_viewer(self) -> None:
        if self.data is not None:
            self.data_viewer.setPlainText(self.data.to_string(index=False))
