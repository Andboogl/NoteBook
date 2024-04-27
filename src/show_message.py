"""Модуль для показу соповіщень на єкран використовуючи QMessageBox"""


from typing import Union
from PyQt6.QtWidgets import QMessageBox
from loguru import logger


def show_message(title: str, text: str) -> None:
    """Показати стандартне соповіщення"""
    message_box = QMessageBox()
    message_box.setWindowTitle(title)
    message_box.setText(text)
    logger.info('Показано стандартне повідомлення')
    message_box.exec()

def show_error_message(text: str, error: Union[str, Exception]) -> None:
    """Показати повідомлення про помилку"""
    message_box = QMessageBox()
    message_box.setDetailedText(str(error))
    message_box.setText(text)
    logger.info('Показано повідомлення про помилку')
    message_box.exec()
