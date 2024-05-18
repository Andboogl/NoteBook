"""Головний файл. Запускає программу"""


from sys import argv
from PyQt6.QtWidgets import QApplication
from loguru import logger
from windows.main_window import MainWindow
from paths import LOG_FILE_PATH


VERSION = '0.1.0'


def main_window():
    """
    Ця функція створює цикл программи QApplication
    та відкриває головне вікно программи
    """
    app = QApplication(argv)
    main_win = MainWindow()
    main_win.design.version.setText(f"Версія {VERSION}")
    main_win.show()
    app.exec()


if __name__ == "__main__":
    # Налаштування логерра
    logger.add(sink=LOG_FILE_PATH)
    logger.success("Логгер успішно налаштований")
    main_window()  # Запуск программи
