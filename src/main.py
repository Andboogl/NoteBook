"""Основний модуль. Запускає программу"""


from PyQt6.QtWidgets import QApplication
from loguru import logger
from main_window import MainWindow
from datetime import datetime
from os.path import expanduser, join
from sys import argv


APP_VERSION = '0.0.0'  # Версія программи


# Налаштування логгера
logger.add(
    sink=join(expanduser('~'),
              '.NoteBook', 'logs',
              f'{datetime.now().strftime("%d.%m.%Y")}.log')
)
logger.debug('Тестовий лог (логгер налаштований)')


def main() -> None:
    """Ця функція запускає додаток"""
    app = QApplication(argv)
    main_window = MainWindow()
    main_window.design.version.setText(f'Версія {APP_VERSION}')
    main_window.show()
    app.exec()


if __name__ == '__main__':
    main()
